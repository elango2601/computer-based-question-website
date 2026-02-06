import json
import os
from flask import Flask, request, jsonify, send_from_directory, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
load_dotenv()
from functools import wraps
from extensions import db
from models import User, Test, Question, Result
from sqlalchemy import func, case

app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = 'secret-key-replace-in-prod'

# Database Config
# Uses DATABASE_URL if found (Postgres on Render), otherwise local sqlite
database_url = os.environ.get('DATABASE_URL', 'sqlite:///database.sqlite')
# Fix for some Postgres providers using 'postgres://' instead of 'postgresql://'
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Production Config for Cookies
if os.environ.get('RENDER'):
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db.init_app(app)

def init_db():
    with app.app_context():
        db.create_all()

# --- Auth Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({"error": "Forbidden"}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400
        
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username taken"}), 400
        
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"success": True})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = user.role
        session['username'] = user.username
        
        return jsonify({
             "success": True, 
             "role": user.role, 
             "username": user.username 
        })
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/me', methods=['GET'])
def me():
    if 'user_id' in session:
        return jsonify({
            "id": session['user_id'], 
            "role": session['role'], 
            "username": session['username']
        })
    return jsonify({"error": "Not logged in"}), 401

# --- Student APIs ---

@app.route('/api/tests', methods=['GET'])
@login_required
def get_tests():
    user_id = session['user_id']
    
    # Get all tests ordered by date
    tests = Test.query.order_by(Test.scheduled_date.asc()).all()
    
    result = []
    for t in tests:
        t_dict = {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "scheduled_date": t.scheduled_date.isoformat() if t.scheduled_date else None,
            "duration_minutes": t.duration_minutes,
            "is_active": t.is_active
        }
        
        # Check if user has attempted this test
        attempt_count = Result.query.filter_by(user_id=user_id, test_id=t.id).count()
        t_dict['is_completed'] = attempt_count > 0
        
        # Calculate scores if completed
        if t_dict['is_completed']:
            total_questions = Result.query.filter_by(user_id=user_id, test_id=t.id).count()
            score = Result.query.filter_by(user_id=user_id, test_id=t.id, is_correct=True).count()
            t_dict['score'] = score
            t_dict['total_questions'] = total_questions
            
        result.append(t_dict)
        
    return jsonify(result)

@app.route('/api/tests/<int:test_id>/questions', methods=['GET'])
@login_required
def get_test_questions(test_id):
    questions = Question.query.filter_by(test_id=test_id).all()
    
    processed = []
    for q in questions:
        q_dict = {
            "id": q.id,
            "text": q.text,
            "type": q.type,
            "category": q.category,
            "difficulty": q.difficulty
        }
        if q.options:
            try:
                q_dict['options'] = json.loads(q.options)
            except:
                q_dict['options'] = []
        processed.append(q_dict)
        
    return jsonify(processed)

@app.route('/api/tests/<int:test_id>/stats', methods=['GET'])
@login_required
def get_test_stats(test_id):
    user_id = session['user_id']
    
    # 1. Basic Counts
    total = Result.query.filter_by(user_id=user_id, test_id=test_id).count()
    score = Result.query.filter_by(user_id=user_id, test_id=test_id, is_correct=True).count()
    
    # 2. History
    # Join Question and Result
    results = db.session.query(Question, Result).\
        outerjoin(Result, (Question.id == Result.question_id) & (Result.user_id == user_id)).\
        filter(Question.test_id == test_id).\
        order_by(Question.id.asc()).all()
    
    history = []
    for q, r in results:
        r_dict = {
            "id": q.id,
            "question_text": q.text,
            "correct_answer": q.correct_answer
        }
        
        if r:
            r_dict['user_answer'] = r.user_answer
            r_dict['is_correct'] = r.is_correct
            r_dict['status'] = 'answered'
            r_dict['timestamp'] = r.timestamp.isoformat() if r.timestamp else None
        else:
            r_dict['user_answer'] = "Not Attempted"
            r_dict['is_correct'] = False
            r_dict['status'] = 'skipped'
            
        history.append(r_dict)
    
    return jsonify({
        "total": total,
        "score": score,
        "history": history
    })

@app.route('/api/submit', methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    question_id = data.get('questionId')
    answer = data.get('answer')
    user_id = session['user_id']
    test_id = data.get('testId')

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
        
    if not test_id:
        test_id = question.test_id

    is_correct = (question.correct_answer == answer)
    
    # Check if result already exists
    existing = Result.query.filter_by(user_id=user_id, question_id=question_id).first()
    
    if existing:
        existing.user_answer = answer
        existing.is_correct = is_correct
        existing.timestamp = func.now()
    else:
        new_result = Result(
            user_id=user_id, 
            test_id=test_id, 
            question_id=question_id, 
            user_answer=answer, 
            is_correct=is_correct
        )
        db.session.add(new_result)
        
    db.session.commit()

    return jsonify({"success": True, "isCorrect": is_correct, "correctAnswer": question.correct_answer})

# --- Admin APIs ---

@app.route('/api/questions', methods=['GET'])
@admin_required
def get_all_questions():
    questions = Question.query.order_by(Question.id.desc()).all()
    processed = []
    for q in questions:
        q_dict = {
            "id": q.id, 
            "text": q.text, 
            "category": q.category, 
            "difficulty": q.difficulty,
            "correct": q.correct_answer
        }
        processed.append(q_dict)
    return jsonify(processed)

@app.route('/api/admin/questions', methods=['POST'])
@admin_required
def add_question():
    data = request.json
    text = data.get('text')
    q_type = data.get('type', 'mcq')
    options = data.get('options', [])
    correct = data.get('correct_answer')
    category = data.get('category', 'General')
    difficulty = data.get('difficulty', 'Medium')
    
    # Get the latest or first test ID if not provided (hacky but functional for now)
    # Ideally should prompt for test_id
    test_id = data.get('test_id')
    if not test_id:
        # Default to whatever matches query or just first test
        # Let's default to the "Active" test (today) or just 1
        test = Test.query.filter_by(is_active=True).first()
        test_id = test.id if test else 1

    if not text or not correct:
        return jsonify({"error": "Missing fields"}), 400

    new_q = Question(
        test_id=test_id,
        text=text,
        type=q_type,
        options=json.dumps(options),
        correct_answer=correct,
        category=category,
        difficulty=difficulty
    )
    
    db.session.add(new_q)
    db.session.commit()
    
    return jsonify({"success": True})

@app.route('/api/admin/questions/<int:q_id>', methods=['DELETE'])
@admin_required
def delete_question(q_id):
    # Cleanup results first
    Result.query.filter_by(question_id=q_id).delete()
    Question.query.filter_by(id=q_id).delete()
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/admin/reset_result/<int:user_id>/<int:test_id>', methods=['DELETE'])
@admin_required
def reset_student_result(user_id, test_id):
    Result.query.filter_by(user_id=user_id, test_id=test_id).delete()
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.filter_by(role='student').all()
    return jsonify([{"id": u.id, "username": u.username} for u in users])

@app.route('/api/admin/student_result/<int:user_id>/<int:test_id>', methods=['GET'])
@admin_required
def admin_student_result(user_id, test_id):
    results = Result.query.filter_by(user_id=user_id, test_id=test_id).all()
    
    if not results:
        return jsonify({'error': 'No results found'}), 404

    # Calculate score
    score = sum(1 for r in results if r.is_correct)
    total = len(results)
    
    # Prepare detailed list
    details = []
    for r in results:
        q = Question.query.get(r.question_id)
        details.append({
            'question_text': q.text if q else "Question Deleted",
            'user_answer': r.user_answer,
            'correct_answer': q.correct_answer if q else "N/A",
            'is_correct': r.is_correct
        })
        
    return jsonify({
        'score': score,
        'total': total,
        'results': details
    })

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def admin_stats():
    # SQLAlchemy Group By Query
    # Select: user.id, user.username, test.title, test.date, test.id, score
    
    results = db.session.query(
        User.id,
        User.username,
        Test.title,
        Test.scheduled_date,
        Test.id,
        func.count(Result.id).label('total_attempted'), # Approximate
        func.sum(case((Result.is_correct == True, 1), else_=0)).label('score')
    ).join(Result, User.id == Result.user_id)\
     .join(Test, Result.test_id == Test.id)\
     .filter(User.role == 'student')\
     .group_by(User.id, User.username, Test.id, Test.title, Test.scheduled_date)\
     .order_by(Test.scheduled_date.desc(), User.username.asc())\
     .all()
     
    stats = []
    for r in results:
        # Get exact total questions for this test to calculate percentage correctly
        total_questions_in_test = Question.query.filter_by(test_id=r[4]).count()
        
        stats.append({
            "userId": r[0],
            "username": r[1],
            "testTitle": r[2],
            "date": r[3].isoformat() if r[3] else None,
            "testId": r[4],
            "score": int(r[6] or 0),
            "totalQuestions": total_questions_in_test
        })
        
    return jsonify(stats)

import seed_data

@app.cli.command("init_db")
def init_db_command():
    db.create_all()
    print("Database initialized.")

@app.cli.command("seed_db")
def seed_db_command():
    seed_data.seed_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Create DB tables if they don't exist
    with app.app_context():
        db.create_all()
        
    print(f"Server running on port {port}")
    app.run(host='0.0.0.0', port=port)
