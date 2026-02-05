import sqlite3
import json
import os
from flask import Flask, request, jsonify, send_from_directory, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = 'secret-key-replace-in-prod'
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite')

# --- Database Helpers ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row  # Return rows that allow access by column name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT DEFAULT 'student',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Questions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                type TEXT, 
                options TEXT,
                correct_answer TEXT,
                category TEXT,
                difficulty TEXT
            )
        ''')

        # Results Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question_id INTEGER,
                user_answer TEXT,
                is_correct BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        ''')
        db.commit()

# --- Auth Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        if session.get('role') != 'admin':
            return jsonify({"error": "Access denied"}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# API: Register
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    hashed_pw = generate_password_hash(password)
    db = get_db()
    try:
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        db.commit()
        return jsonify({"success": True, "message": "User registered successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "error": "Username already exists"}), 400

# API: Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['role'] = user['role']
        session['username'] = user['username']
        return jsonify({"success": True, "role": user['role'], "username": user['username']})
    
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

# API: Logout
@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

# API: Get User Info
@app.route('/api/me', methods=['GET'])
@login_required
def me():
    return jsonify({
        "userId": session.get('user_id'),
        "username": session.get('username'),
        "role": session.get('role')
    })

# API: Get Questions (Student)
@app.route('/api/questions', methods=['GET'])
@login_required
def get_questions():
    db = get_db()
    questions = db.execute("SELECT id, text, type, options, category, difficulty FROM questions").fetchall()
    
    processed = []
    for q in questions:
        q_dict = dict(q)
        if q_dict['options']:
            try:
                q_dict['options'] = json.loads(q_dict['options'])
            except:
                q_dict['options'] = []
        processed.append(q_dict)
        
    return jsonify(processed)

# API: Submit Answer
@app.route('/api/submit', methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    question_id = data.get('questionId')
    answer = data.get('answer')
    user_id = session['user_id']

    db = get_db()
    question = db.execute("SELECT correct_answer FROM questions WHERE id = ?", (question_id,)).fetchone()
    
    if not question:
        return jsonify({"error": "Question not found"}), 404

    is_correct = (question['correct_answer'] == answer)
    
    db.execute("INSERT INTO results (user_id, question_id, user_answer, is_correct) VALUES (?, ?, ?, ?)",
               (user_id, question_id, answer, is_correct))
    db.commit()

    return jsonify({"success": True, "isCorrect": is_correct, "correctAnswer": question['correct_answer']})

# API: User Stats (Detailed Solutions)
@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    user_id = session['user_id']
    db = get_db()
    
    # 1. Basic Counts
    total = db.execute("SELECT COUNT(*) as count FROM results WHERE user_id = ?", (user_id,)).fetchone()['count']
    score = db.execute("SELECT COUNT(*) as count FROM results WHERE user_id = ? AND is_correct = 1", (user_id,)).fetchone()['count']
    
    # 2. Full History (All Questions + Latest Attempt)
    # This query fetches ALL questions and joins with the student's LATEST attempt for each.
    query = '''
        SELECT q.id, q.text as question_text, q.correct_answer, 
               r.user_answer, r.is_correct, r.timestamp
        FROM questions q
        LEFT JOIN (
            SELECT r1.*
            FROM results r1
            INNER JOIN (
                SELECT question_id, MAX(id) as max_id
                FROM results
                WHERE user_id = ?
                GROUP BY question_id
            ) r2 ON r1.id = r2.max_id
        ) r ON q.id = r.question_id
        ORDER BY q.id ASC
    '''
    
    detailed_rows = db.execute(query, (user_id,)).fetchall()
    
    # Process rows
    history = []
    for row in detailed_rows:
        r_dict = dict(row)
        # Handle Unanswered
        if r_dict['user_answer'] is None:
             r_dict['user_answer'] = "Not Attempted"
             r_dict['is_correct'] = False
             r_dict['status'] = 'skipped'
        else:
            r_dict['status'] = 'answered'
            r_dict['is_correct'] = bool(r_dict['is_correct']) # Ensure boolean
            
        history.append(r_dict)
    
    return jsonify({
        "total": total,
        "score": score,
        "history": history
    })

# API: Admin Stats
@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def admin_stats():
    db = get_db()
    users = db.execute("SELECT id, username, role FROM users WHERE role != 'admin'").fetchall()
    
    stats = []
    for user in users:
        res = db.execute("SELECT COUNT(*) as total, SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as score FROM results WHERE user_id = ?", (user['id'],)).fetchone()
        stats.append({
            "username": user['username'],
            "totalAnswered": res['total'],
            "score": res['score'] if res['score'] else 0
        })
        
    return jsonify(stats)

if __name__ == '__main__':
    # Only run seeds if DB doesn't exist (basic check)
    if not os.path.exists(DB_PATH):
        try:
            from seed import seed
            seed()
        except:
            pass
            
    port = int(os.environ.get('PORT', 3000))
    # Debug mode is False by default in production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
