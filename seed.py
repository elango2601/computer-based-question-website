import sqlite3
import json
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite')

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'student',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            scheduled_date DATE,
            duration_minutes INTEGER DEFAULT 60,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER,
            text TEXT,
            type TEXT, 
            options TEXT,
            correct_answer TEXT,
            category TEXT,
            difficulty TEXT,
            FOREIGN KEY (test_id) REFERENCES tests(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            test_id INTEGER,
            question_id INTEGER,
            user_answer TEXT,
            is_correct BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (test_id) REFERENCES tests(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')

    # ADMIN
    admin = cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',)).fetchone()
    if not admin:
        hash_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', hash_pw, 'admin'))
        print("Admin user created.")

    # STUDENT
    student = cursor.execute("SELECT * FROM users WHERE username = ?", ('student',)).fetchone()
    if not student:
        hash_pw = generate_password_hash('student123')
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('student', hash_pw, 'student'))
        print("Student user created.")

    # QUESTIONS
    # Clear existing questions to update with the new bank
    # TESTS
    cursor.execute("DELETE FROM tests")
    
    # Calculate dates: Yesterday, Today, Tomorrow
    import datetime
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    day_after = today + datetime.timedelta(days=2)
    
    tests_data = [
        ("Maths Phase 1 (Units 1-4)", "Topics: Matrices, Complex Numbers, Theory of Eq, Inv. Trig", today),
        ("Maths Phase 2 (Units 5-8)", "Topics: 2D Analytical Geo, Vector Algebra, Applications", tomorrow),
        ("Maths Phase 3 (Units 9-12)", "Topics: Calculus, Probability, Discrete Math", day_after)
    ]
    
    test_ids = []
    for t in tests_data:
        cursor.execute("INSERT INTO tests (title, description, scheduled_date) VALUES (?, ?, ?)", t)
        test_ids.append(cursor.lastrowid)
        
    print(f"Created {len(test_ids)} tests.")

    # QUESTIONS
    # Clear existing questions to update with the new bank
    cursor.execute("DELETE FROM questions")
    
    # NOTE: All current seeded questions belong to Phase 1 (Units 1-4)
    # So we assign everything to test_idx: 0
    questions_list = [
        # Unit 1 - Matrices
        {
            "text": "If A = [2 1; 0 5] and B = [1 4; 2 0], then |adj(AB)| =",
            "type": "mcq",
            "options": ["-40", "-80", "-60", "-20"],
            "correct": "-80",
            "cat": "App of Matrices",
            "diff": "Medium",
            "test_idx": 0
        },
        {
            "text": "If A = [7 3; 4 2], then 9I - A =",
            "type": "mcq",
            "options": ["A⁻¹", "(A⁻¹)/2", "3A⁻¹", "2A⁻¹"],
            "correct": "2A⁻¹",
            "cat": "App of Matrices",
            "diff": "Medium",
            "test_idx": 0
        },
        {
            "text": "The rank of the matrix [[1, 2, -1], [2, 4, -2], [3, 6, -3], [4, 8, -4]] is",
            "type": "mcq",
            "options": ["1", "2", "3", "4"],
            "correct": "1",
            "cat": "App of Matrices",
            "diff": "Easy",
            "test_idx": 0
        },
        {
            "text": "If A = [3 1; 5 2], B = adj(A) and C = 3A, then |adj(B)|/|C| =",
            "type": "mcq",
            "options": ["1/3", "1/9", "1/4", "1"],
            "correct": "1/9",
            "cat": "App of Matrices",
            "diff": "Hard",
            "test_idx": 0
        },
        {
            "text": "If the inverse of [1 3; 2 -5] is (1/11)[a c; b d], then the ascending order of a,b,c,d is",
            "type": "mcq",
            "options": ["a, b, c, d", "d, b, c, a", "c, a, b, d", "b, a, c, d"],
            "correct": "d, b, c, a",
            "cat": "App of Matrices",
            "diff": "Hard",
            "test_idx": 0
        },
        {
            "text": "The rank of a singular matrix is",
            "type": "mcq",
            "options": ["always zero", "always one", "less than its order", "equal to its order"],
            "correct": "less than its order",
            "cat": "App of Matrices",
            "diff": "Easy",
            "test_idx": 0
        },
        {
            "text": "If |A| = 0, then",
            "type": "mcq",
            "options": ["A⁻¹ exists", "A is non-singular", "A is singular", "adj(A) does not exist"],
            "correct": "A is singular",
            "cat": "App of Matrices",
            "diff": "Easy",
            "test_idx": 0
        },
        {
            "text": "If A is a non-singular square matrix, then",
            "type": "mcq",
            "options": ["AA⁻¹ = 0", "AA⁻¹ = I", "A⁻¹A = 0", "A + A⁻¹ = I"],
            "correct": "AA⁻¹ = I",
            "cat": "App of Matrices",
            "diff": "Easy",
            "test_idx": 0
        },
        
        # Unit 2 - Complex Numbers
        {
            "text": "i^n + i^(n+1) + i^(n+2) + i^(n+3) =",
            "type": "mcq",
            "options": ["0", "1", "-1", "i"],
            "correct": "0",
            "cat": "Complex Numbers",
            "diff": "Easy",
            "test_idx": 0
        },
        {
            "text": "If (1+i)(1+2i)...(1+ni) = x+iy, then 1² + 2² + ... + n² =",
            "type": "mcq",
            "options": ["1", "i", "x² + y²", "1 + n²"],
            "correct": "x² + y²",
            "cat": "Complex Numbers",
            "diff": "Medium", 
            "test_idx": 0
        },
        {
            "text": "If p + iq = (2 - 3i)(4 + 2i), then q =",
            "type": "mcq",
            "options": ["14", "-14", "-8", "8"],
            "correct": "-8",
            "cat": "Complex Numbers",
            "diff": "Medium",
            "test_idx": 0
        },
        {
            "text": "If |z + 1/z| is minimum, then the least value of |z| is",
            "type": "mcq",
            "options": ["1", "2", "3", "5"],
            "correct": "1",
            "cat": "Complex Numbers",
            "diff": "Hard",
            "test_idx": 0
        },
        {
            "text": "The principal argument of -1 + i is",
            "type": "mcq",
            "options": ["π/4", "-π/4", "-3π/4", "3π/4"],
            "correct": "3π/4",
            "cat": "Complex Numbers",
            "diff": "Medium",
            "test_idx": 0
        },
        {
            "text": "The product of all four values of (cos(π/3) + i sin(π/3))^(3/4) is",
            "type": "mcq",
            "options": ["-2", "-1", "1", "2"],
            "correct": "1",
            "cat": "Complex Numbers",
            "diff": "Hard",
            "test_idx": 0
        },
        
        # Unit 3 - Theory of Equations
        {
            "text": "A zero of x^3 + 64 = 0 is",
            "type": "mcq",
            "options": ["0", "4", "4i", "-4"],
            "correct": "-4",
            "cat": "Theory of Equations",
            "diff": "Easy",
            "test_idx": 0
        },
        {
            "text": "The equation x^3 + 2x + 3 = 0 has",
            "type": "mcq",
            "options": ["one negative and two imaginary roots", "one positive and two imaginary roots", "three real roots", "no roots"],
            "correct": "one negative and two imaginary roots",
            "cat": "Theory of Equations",
            "diff": "Medium",
            "test_idx": 0
        },
        {
            "text": "If all roots of a polynomial are real and unequal, its discriminant is",
            "type": "mcq",
            "options": ["zero", "positive", "negative", "imaginary"],
            "correct": "positive",
            "cat": "Theory of Equations",
            "diff": "Medium",
            "test_idx": 0
        },
        {
            "text": "The product of roots of x^3 + px^2 + qx + r = 0 is",
            "type": "mcq",
            "options": ["p", "q", "-r", "r"],
            "correct": "-r",
            "cat": "Theory of Equations",
            "diff": "Easy",
            "test_idx": 0
        },
        
        # Unit 4 - Inv. Trigonometry
        {
            "text": "sin⁻¹(cos x) = π/2 - x is valid for",
            "type": "mcq",
            "options": ["-π ≤ x ≤ 0", "0 ≤ x ≤ π", "-π/2 ≤ x ≤ π/2", "-π/4 ≤ x ≤ 3π/4"],
            "correct": "0 ≤ x ≤ π",
            "cat": "Inv. Trigonometry",
            "diff": "Hard",
            "test_idx": 0
        },
        {
            "text": "tan⁻¹ x + cot⁻¹ x =",
            "type": "mcq",
            "options": ["1", "-π", "π/2", "π"],
            "correct": "π/2",
            "cat": "Inv. Trigonometry",
            "diff": "Easy",
            "test_idx": 0
        },
        {
            "text": "sin⁻¹(2cos²A - 1) + cos⁻¹(1 - 2sin²A) =",
            "type": "mcq",
            "options": ["π/2", "π/3", "π/4", "π/6"],
            "correct": "π/2",
            "cat": "Inv. Trigonometry",
            "diff": "Medium",
            "test_idx": 0
        },
        {
            "text": "If cot⁻¹ x = 2π/5, then tan⁻¹ x =",
            "type": "mcq",
            "options": ["-π/10", "π/5", "π/10", "-π/5"],
            "correct": "π/10",
            "cat": "Inv. Trigonometry",
            "diff": "Medium",
            "test_idx": 0
        }
    ]

    print(f"Adding {len(questions_list)} questions...")
    for q in questions_list:
        test_id = test_ids[q['test_idx']]
        cursor.execute(
            "INSERT INTO questions (test_id, text, type, options, correct_answer, category, difficulty) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (test_id, q['text'], q['type'], json.dumps(q['options']), q['correct'], q['cat'], q['diff'])
        )

    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == '__main__':
    seed()
