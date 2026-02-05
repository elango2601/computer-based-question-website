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
    
    questions_list = [
        # UNIT 1 - Matrices (15 MCQs)
        {"text": "If A = [2 1; 0 5] and B = [1 4; 2 0], then |adj(AB)| =", "type": "mcq", "options": ["-40", "-80", "-60", "-20"], "correct": "-80", "cat": "App of Matrices", "diff": "Medium", "test_idx": 0},
        {"text": "If A = [7 3; 4 2], then 9I - A =", "type": "mcq", "options": ["A⁻¹", "(A⁻¹)/2", "3A⁻¹", "2A⁻¹"], "correct": "2A⁻¹", "cat": "App of Matrices", "diff": "Medium", "test_idx": 0},
        {"text": "The rank of the matrix [[1, 2, -1], [2, 4, -2], [3, 6, -3], [4, 8, -4]] is", "type": "mcq", "options": ["1", "2", "3", "4"], "correct": "1", "cat": "App of Matrices", "diff": "Easy", "test_idx": 0},
        {"text": "If |A| = 0, then A is", "type": "mcq", "options": ["non-singular", "identity", "singular", "orthogonal"], "correct": "singular", "cat": "App of Matrices", "diff": "Easy", "test_idx": 0},
        {"text": "If A² = A, then A is", "type": "mcq", "options": ["symmetric", "idempotent", "skew-symmetric", "singular"], "correct": "idempotent", "cat": "App of Matrices", "diff": "Medium", "test_idx": 0},
        {"text": "If A is non-singular, then", "type": "mcq", "options": ["|A| = 0", "adj(A) = 0", "rank(A) = order(A)", "A has no inverse"], "correct": "rank(A) = order(A)", "cat": "App of Matrices", "diff": "Medium", "test_idx": 0},
        {"text": "Order of adj(A) for a square matrix of order 3 is", "type": "mcq", "options": ["2×2", "3×3", "1×3", "3×1"], "correct": "3×3", "cat": "App of Matrices", "diff": "Easy", "test_idx": 0},
        {"text": "If A is singular, then", "type": "mcq", "options": ["adj(A) exists", "A⁻¹ exists", "|A| ≠ 0", "rank(A) = order(A)"], "correct": "adj(A) exists", "cat": "App of Matrices", "diff": "Medium", "test_idx": 0},
        {"text": "If A · adj(A) = kI, then k equals", "type": "mcq", "options": ["0", "1", "|A|", "adj(A)"], "correct": "|A|", "cat": "App of Matrices", "diff": "Medium", "test_idx": 0},
        {"text": "If A is non-singular, then A⁻¹ equals", "type": "mcq", "options": ["adj(A)", "|A|adj(A)", "adj(A)/|A|", "|A|/adj(A)"], "correct": "adj(A)/|A|", "cat": "App of Matrices", "diff": "Medium", "test_idx": 0},
        {"text": "Rank of identity matrix of order n is", "type": "mcq", "options": ["0", "1", "n", "n²"], "correct": "n", "cat": "App of Matrices", "diff": "Easy", "test_idx": 0},
        {"text": "If rank(A) = order(A), then A is", "type": "mcq", "options": ["singular", "non-singular", "zero matrix", "scalar matrix"], "correct": "non-singular", "cat": "App of Matrices", "diff": "Easy", "test_idx": 0},
        {"text": "Determinant of adj(A) for 2×2 matrix A is", "type": "mcq", "options": ["|A|", "|A|²", "1", "|A|⁻¹"], "correct": "|A|", "cat": "App of Matrices", "diff": "Easy", "test_idx": 0},
        {"text": "If A is zero matrix, then rank(A) =", "type": "mcq", "options": ["0", "1", "2", "undefined"], "correct": "0", "cat": "App of Matrices", "diff": "Easy", "test_idx": 0},
        {"text": "If |A| ≠ 0, then A has", "type": "mcq", "options": ["no solution", "unique inverse", "infinite inverses", "zero inverse"], "correct": "unique inverse", "cat": "App of Matrices", "diff": "Easy", "test_idx": 0},

        # UNIT 2 - Complex Numbers (15 MCQs)
        {"text": "i^n + i^(n+1) + i^(n+2) + i^(n+3) =", "type": "mcq", "options": ["0", "1", "-1", "i"], "correct": "0", "cat": "Complex Numbers", "diff": "Easy", "test_idx": 0},
        {"text": "If z = 3 - 4i, then |z| =", "type": "mcq", "options": ["5", "7", "√7", "25"], "correct": "5", "cat": "Complex Numbers", "diff": "Easy", "test_idx": 0},
        {"text": "If z·z̄ = 25, then |z| =", "type": "mcq", "options": ["5", "-5", "25", "√5"], "correct": "5", "cat": "Complex Numbers", "diff": "Easy", "test_idx": 0},
        {"text": "Argument of a negative real number is", "type": "mcq", "options": ["0", "π", "π/2", "-π/2"], "correct": "π", "cat": "Complex Numbers", "diff": "Easy", "test_idx": 0},
        {"text": "The principal argument of -1 + i is", "type": "mcq", "options": ["π/4", "-π/4", "-3π/4", "3π/4"], "correct": "3π/4", "cat": "Complex Numbers", "diff": "Medium", "test_idx": 0},
        {"text": "If z + 1/z ∈ R and z ∉ R, then |z| =", "type": "mcq", "options": ["0", "1", "2", "3"], "correct": "1", "cat": "Complex Numbers", "diff": "Hard", "test_idx": 0},
        {"text": "The modulus of (1-i)/(1+i) is", "type": "mcq", "options": ["0", "1", "√2", "2"], "correct": "1", "cat": "Complex Numbers", "diff": "Medium", "test_idx": 0},
        {"text": "If z = cos θ + i sin θ, then z·z̄ =", "type": "mcq", "options": ["0", "i", "1", "-1"], "correct": "1", "cat": "Complex Numbers", "diff": "Medium", "test_idx": 0},
        {"text": "The least value of n for which (√3/2 + i/2)^n = 1 is", "type": "mcq", "options": ["30", "24", "12", "18"], "correct": "12", "cat": "Complex Numbers", "diff": "Hard", "test_idx": 0},
        {"text": "Roots of z^n = 1 are called", "type": "mcq", "options": ["imaginary roots", "real roots", "roots of unity", "irrational roots"], "correct": "roots of unity", "cat": "Complex Numbers", "diff": "Easy", "test_idx": 0},
        {"text": "The product of all roots of unity is", "type": "mcq", "options": ["-1", "0", "1", "i"], "correct": "1", "cat": "Complex Numbers", "diff": "Medium", "test_idx": 0},
        {"text": "|z|² equals", "type": "mcq", "options": ["z²", "z̄²", "z·z̄", "z + z̄"], "correct": "z·z̄", "cat": "Complex Numbers", "diff": "Easy", "test_idx": 0},
        {"text": "Argument of positive real number is", "type": "mcq", "options": ["π", "π/2", "0", "-π"], "correct": "0", "cat": "Complex Numbers", "diff": "Easy", "test_idx": 0},
        {"text": "If ω = cis(2π/3), then ω³ equals", "type": "mcq", "options": ["1", "-1", "i", "-i"], "correct": "1", "cat": "Complex Numbers", "diff": "Medium", "test_idx": 0},
        {"text": "The number of cube roots of unity is", "type": "mcq", "options": ["1", "2", "3", "4"], "correct": "3", "cat": "Complex Numbers", "diff": "Easy", "test_idx": 0},

        # UNIT 3 - Theory of Equations (15 MCQs)
        {"text": "A zero of x^3 + 64 is", "type": "mcq", "options": ["0", "4", "4i", "-4"], "correct": "-4", "cat": "Theory of Equations", "diff": "Easy", "test_idx": 0},
        {"text": "If coefficients are real and one root is 2+i, another root is", "type": "mcq", "options": ["2-i", "-2+i", "-2-i", "1-i"], "correct": "2-i", "cat": "Theory of Equations", "diff": "Easy", "test_idx": 0},
        {"text": "Sum of roots of x^3 - 5x^2 + 6x - 2 = 0 is", "type": "mcq", "options": ["2", "5", "-5", "6"], "correct": "5", "cat": "Theory of Equations", "diff": "Medium", "test_idx": 0},
        {"text": "Product of roots of x^3 + px^2 + qx + r = 0 is", "type": "mcq", "options": ["p", "q", "r", "-r"], "correct": "-r", "cat": "Theory of Equations", "diff": "Easy", "test_idx": 0},
        {"text": "If all roots are real and unequal, discriminant is", "type": "mcq", "options": ["0", "negative", "positive", "imaginary"], "correct": "positive", "cat": "Theory of Equations", "diff": "Medium", "test_idx": 0},
        {"text": "Descartes’ rule gives information about", "type": "mcq", "options": ["total roots", "imaginary roots", "positive & negative roots", "equal roots"], "correct": "positive & negative roots", "cat": "Theory of Equations", "diff": "Easy", "test_idx": 0},
        {"text": "A cubic equation has at least", "type": "mcq", "options": ["one real root", "two real roots", "three imaginary roots", "no real root"], "correct": "one real root", "cat": "Theory of Equations", "diff": "Easy", "test_idx": 0},
        {"text": "If one root is irrational, then", "type": "mcq", "options": ["all are irrational", "at least two are irrational", "all are real", "one is imaginary"], "correct": "at least two are irrational", "cat": "Theory of Equations", "diff": "Medium", "test_idx": 0},
        {"text": "Nature of roots depends on", "type": "mcq", "options": ["degree", "coefficients", "discriminant", "variable"], "correct": "discriminant", "cat": "Theory of Equations", "diff": "Easy", "test_idx": 0},
        {"text": "If discriminant is zero, roots are", "type": "mcq", "options": ["distinct", "unequal", "repeated", "imaginary"], "correct": "repeated", "cat": "Theory of Equations", "diff": "Medium", "test_idx": 0},
        {"text": "Equation x^3 + 2x + 3 = 0 has", "type": "mcq", "options": ["three real roots", "one real, two imaginary", "all imaginary", "no roots"], "correct": "one real, two imaginary", "cat": "Theory of Equations", "diff": "Hard", "test_idx": 0},
        {"text": "If sum of roots is zero, coefficient of x^2 is", "type": "mcq", "options": ["1", "0", "-1", "undefined"], "correct": "0", "cat": "Theory of Equations", "diff": "Medium", "test_idx": 0},
        {"text": "Polynomial of degree n has at most", "type": "mcq", "options": ["n roots", "n-1 roots", "n+1 roots", "infinite roots"], "correct": "n roots", "cat": "Theory of Equations", "diff": "Easy", "test_idx": 0},
        {"text": "If α, β are roots, then equation with roots -α, -β is obtained by", "type": "mcq", "options": ["replacing x by -x", "multiplying by -1", "squaring", "dividing"], "correct": "replacing x by -x", "cat": "Theory of Equations", "diff": "Medium", "test_idx": 0},
        {"text": "If coefficients are symmetric, roots are", "type": "mcq", "options": ["equal", "reciprocal", "imaginary", "zero"], "correct": "reciprocal", "cat": "Theory of Equations", "diff": "Medium", "test_idx": 0},

        # UNIT 4 - Inverse Trigonometric Functions (15 MCQs)
        {"text": "Principal value range of sin⁻¹x is", "type": "mcq", "options": ["[0,π]", "[-π/2,π/2]", "[-π,π]", "[0,2π]"], "correct": "[-π/2,π/2]", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "Principal value of cos⁻¹x lies in", "type": "mcq", "options": ["[0,π]", "[-π/2,π/2]", "[-π,π]", "[0,2π]"], "correct": "[0,π]", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "tan⁻¹x + cot⁻¹x equals", "type": "mcq", "options": ["π", "π/2", "0", "1"], "correct": "π/2", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "sin⁻¹(1) equals", "type": "mcq", "options": ["0", "π", "π/2", "-π/2"], "correct": "π/2", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "cos⁻¹(-1) equals", "type": "mcq", "options": ["0", "π", "π/2", "-π"], "correct": "π", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "tan⁻¹(∞) equals", "type": "mcq", "options": ["0", "π", "π/2", "-π/2"], "correct": "π/2", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "sin⁻¹x + cos⁻¹x equals", "type": "mcq", "options": ["π", "π/2", "0", "2π"], "correct": "π/2", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "Domain of sin⁻¹x is", "type": "mcq", "options": ["ℝ", "(-∞,∞)", "[-1,1]", "(0,1)"], "correct": "[-1,1]", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "Range of tan⁻¹x is", "type": "mcq", "options": ["(-π/2,π/2)", "(0,π)", "[-π,π]", "[0,2π]"], "correct": "(-π/2,π/2)", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "cos⁻¹0 equals", "type": "mcq", "options": ["0", "π", "π/2", "-π/2"], "correct": "π/2", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "sin⁻¹0 equals", "type": "mcq", "options": ["0", "π", "π/2", "-π/2"], "correct": "0", "cat": "Inv. Trigonometry", "diff": "Easy", "test_idx": 0},
        {"text": "If x∈[-1,1], then sin⁻¹x exists because", "type": "mcq", "options": ["sine is periodic", "sine is bounded", "sine is odd", "sine is continuous"], "correct": "sine is bounded", "cat": "Inv. Trigonometry", "diff": "Medium", "test_idx": 0},
        {"text": "sin⁻¹(cos x)=π/2-x is valid for", "type": "mcq", "options": ["-π≤x≤0", "0≤x≤π", "-π/2≤x≤π/2", "-π≤x≤π"], "correct": "0≤x≤π", "cat": "Inv. Trigonometry", "diff": "Hard", "test_idx": 0},
        {"text": "If cot⁻¹x=2π/5, then tan⁻¹x=", "type": "mcq", "options": ["-π/10", "π/5", "π/10", "-π/5"], "correct": "π/10", "cat": "Inv. Trigonometry", "diff": "Medium", "test_idx": 0},
        {"text": "sin⁻¹x + sin⁻¹y = 2π/3 ⇒ cos⁻¹x + cos⁻¹y equals", "type": "mcq", "options": ["2π/3", "π/3", "π/6", "π"], "correct": "π/3", "cat": "Inv. Trigonometry", "diff": "Hard", "test_idx": 0}
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
