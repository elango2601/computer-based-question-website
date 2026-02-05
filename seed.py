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
    cursor.execute("DELETE FROM questions")
    
    questions_list = [
        # Unit 1 - Matrices (Previous)
        {
            "text": "If A = [2 1; 0 5] and B = [1 4; 2 0], then |adj(AB)| =",
            "type": "mcq",
            "options": ["-40", "-80", "-60", "-20"],
            "correct": "-80",
            "cat": "App of Matrices",
            "diff": "Medium"
        },
        {
            "text": "If A = [7 3; 4 2], then 9I - A =",
            "type": "mcq",
            "options": ["A⁻¹", "(A⁻¹)/2", "3A⁻¹", "2A⁻¹"],
            "correct": "2A⁻¹",
            "cat": "App of Matrices",
            "diff": "Medium"
        },
        {
            "text": "The rank of the matrix [[1, 2, -1], [2, 4, -2], [3, 6, -3], [4, 8, -4]] is",
            "type": "mcq",
            "options": ["1", "2", "3", "4"],
            "correct": "1",
            "cat": "App of Matrices",
            "diff": "Easy"
        },
        {
            "text": "If A = [3 1; 5 2], B = adj(A) and C = 3A, then |adj(B)|/|C| =",
            "type": "mcq",
            "options": ["1/3", "1/9", "1/4", "1"],
            "correct": "1/9",
            "cat": "App of Matrices",
            "diff": "Hard"
        },
        {
            "text": "If the inverse of [1 3; 2 -5] is (1/11)[a c; b d], then the ascending order of a,b,c,d is",
            "type": "mcq",
            "options": ["a, b, c, d", "d, b, c, a", "c, a, b, d", "b, a, c, d"],
            "correct": "d, b, c, a",
            "cat": "App of Matrices",
            "diff": "Hard"
        },
        {
            "text": "The rank of a singular matrix is",
            "type": "mcq",
            "options": ["always zero", "always one", "less than its order", "equal to its order"],
            "correct": "less than its order",
            "cat": "App of Matrices",
            "diff": "Easy"
        },
        {
            "text": "If |A| = 0, then",
            "type": "mcq",
            "options": ["A⁻¹ exists", "A is non-singular", "A is singular", "adj(A) does not exist"],
            "correct": "A is singular",
            "cat": "App of Matrices",
            "diff": "Easy"
        },
        {
            "text": "If A is a non-singular square matrix, then",
            "type": "mcq",
            "options": ["AA⁻¹ = 0", "AA⁻¹ = I", "A⁻¹A = 0", "A + A⁻¹ = I"],
            "correct": "AA⁻¹ = I",
            "cat": "App of Matrices",
            "diff": "Easy"
        },
        {
            "text": "The determinant of adj(A), where A is a 2×2 matrix, is",
            "type": "mcq",
            "options": ["|A|", "|A|²", "|A|⁻¹", "1"],
            "correct": "|A|",
            "cat": "App of Matrices",
            "diff": "Medium"
        },
        
        # Unit 2 - Complex Numbers (Previous)
        {
            "text": "i^n + i^(n+1) + i^(n+2) + i^(n+3) =",
            "type": "mcq",
            "options": ["0", "1", "-1", "i"],
            "correct": "0",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        {
            "text": "If (1+i)(1+2i)...(1+ni) = x+iy, then 1² + 2² + ... + n² =",
            "type": "mcq",
            "options": ["1", "i", "x² + y²", "1 + n²"],
            "correct": "x² + y²",
            "cat": "Complex Numbers",
            "diff": "Medium"
        },
        {
            "text": "If p + iq = (2 - 3i)(4 + 2i), then q =",
            "type": "mcq",
            "options": ["14", "-14", "-8", "8"],
            "correct": "-8",
            "cat": "Complex Numbers",
            "diff": "Medium"
        },
        {
            "text": "If |z + 1/z| is minimum, then the least value of |z| is",
            "type": "mcq",
            "options": ["1", "2", "3", "5"],
            "correct": "1",
            "cat": "Complex Numbers",
            "diff": "Hard"
        },
        {
            "text": "The principal argument of -1 + i is",
            "type": "mcq",
            "options": ["π/4", "-π/4", "-3π/4", "3π/4"],
            "correct": "3π/4",
            "cat": "Complex Numbers",
            "diff": "Medium"
        },
        {
            "text": "The product of all four values of (cos(π/3) + i sin(π/3))^(3/4) is",
            "type": "mcq",
            "options": ["-2", "-1", "1", "2"],
            "correct": "1",
            "cat": "Complex Numbers",
            "diff": "Hard"
        },
        {
            "text": "The least value of n satisfying (√3/2 + i/2)^n = 1 is",
            "type": "mcq",
            "options": ["30", "24", "12", "18"],
            "correct": "12",
            "cat": "Complex Numbers",
            "diff": "Medium"
        },
        {
            "text": "If z ∈ C\\R and z + 1/z ∈ R, then |z| =",
            "type": "mcq",
            "options": ["0", "1", "2", "3"],
            "correct": "1",
            "cat": "Complex Numbers",
            "diff": "Hard"
        },
        {
            "text": "The value of cos⁻¹(-1) + tan⁻¹(∞) + sin⁻¹(1) is",
            "type": "mcq",
            "options": ["3π/2", "-π", "2π", "3π"],
            "correct": "2π",
            "cat": "Complex Numbers",
            "diff": "Medium"
        },
        {
            "text": "The value of sin⁻¹(1) + sin⁻¹(0) is",
            "type": "mcq",
            "options": ["π/2", "0", "1", "π"],
            "correct": "π/2",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        {
            "text": "If z = cos θ + i sin θ, then |z| =",
            "type": "mcq",
            "options": ["0", "1", "θ", "π"],
            "correct": "1",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        {
            "text": "If z^n = 1, then the roots are called",
            "type": "mcq",
            "options": ["imaginary roots", "real roots", "roots of unity", "irrational roots"],
            "correct": "roots of unity",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        {
            "text": "The argument of a positive real number is",
            "type": "mcq",
            "options": ["π", "π/2", "0", "-π"],
            "correct": "0",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        {
            "text": "If z·z̄ = 25, then |z| =",
            "type": "mcq",
            "options": ["5", "10", "25", "√5"],
            "correct": "5",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        
        # Unit 3 - Theory of Equations (Previous)
        {
            "text": "A zero of x^3 + 64 = 0 is",
            "type": "mcq",
            "options": ["0", "4", "4i", "-4"],
            "correct": "-4",
            "cat": "Theory of Equations",
            "diff": "Easy"
        },
        {
            "text": "The equation x^3 + 2x + 3 = 0 has",
            "type": "mcq",
            "options": ["one negative and two imaginary roots", "one positive and two imaginary roots", "three real roots", "no roots"],
            "correct": "one negative and two imaginary roots",
            "cat": "Theory of Equations",
            "diff": "Medium"
        },
        {
            "text": "If all roots of a polynomial are real and unequal, its discriminant is",
            "type": "mcq",
            "options": ["zero", "positive", "negative", "imaginary"],
            "correct": "positive",
            "cat": "Theory of Equations",
            "diff": "Medium"
        },
        {
            "text": "The product of roots of x^3 + px^2 + qx + r = 0 is",
            "type": "mcq",
            "options": ["p", "q", "-r", "r"],
            "correct": "-r",
            "cat": "Theory of Equations",
            "diff": "Easy"
        },
        {
            "text": "If one root of a polynomial equation with real coefficients is complex, then",
            "type": "mcq",
            "options": ["all roots are complex", "all roots are real", "its conjugate is also a root", "it has no real root"],
            "correct": "its conjugate is also a root",
            "cat": "Theory of Equations",
            "diff": "Easy"
        },
        {
            "text": "Descartes’ rule of signs is used to find",
            "type": "mcq",
            "options": ["number of roots", "nature of roots", "positive and negative roots", "imaginary roots"],
            "correct": "nature of roots",
            "cat": "Theory of Equations",
            "diff": "Easy"
        },
        
        # Unit 4 - Inv. Trigonometry (Previous)
        {
            "text": "sin⁻¹(cos x) = π/2 - x is valid for",
            "type": "mcq",
            "options": ["-π ≤ x ≤ 0", "0 ≤ x ≤ π", "-π/2 ≤ x ≤ π/2", "-π/4 ≤ x ≤ 3π/4"],
            "correct": "0 ≤ x ≤ π",
            "cat": "Inv. Trigonometry",
            "diff": "Hard"
        },
        {
            "text": "tan⁻¹ x + cot⁻¹ x =",
            "type": "mcq",
            "options": ["1", "-π", "π/2", "π"],
            "correct": "π/2",
            "cat": "Inv. Trigonometry",
            "diff": "Easy"
        },
        {
            "text": "sin⁻¹(2cos²A - 1) + cos⁻¹(1 - 2sin²A) =",
            "type": "mcq",
            "options": ["π/2", "π/3", "π/4", "π/6"],
            "correct": "π/2",
            "cat": "Inv. Trigonometry",
            "diff": "Medium"
        },
        {
            "text": "If cot⁻¹ x = 2π/5, then tan⁻¹ x =",
            "type": "mcq",
            "options": ["-π/10", "π/5", "π/10", "-π/5"],
            "correct": "π/10",
            "cat": "Inv. Trigonometry",
            "diff": "Medium"
        },
        {
            "text": "If sin⁻¹ x + sin⁻¹ y = 2π/3, then cos⁻¹ x + cos⁻¹ y =",
            "type": "mcq",
            "options": ["2π/3", "π/3", "π/6", "π"],
            "correct": "π/3",
            "cat": "Inv. Trigonometry",
            "diff": "Medium"
        },
        {
            "text": "The domain of f(x) = sin⁻¹ x - 1 is",
            "type": "mcq",
            "options": ["[1, 2]", "[-1, 1]", "[0, 1]", "[-1, 0]"],
            "correct": "[-1, 1]",
            "cat": "Inv. Trigonometry",
            "diff": "Easy"
        },
        {
            "text": "tan⁻¹(∞) =",
            "type": "mcq",
            "options": ["0", "π", "π/2", "-π/2"],
            "correct": "π/2",
            "cat": "Inv. Trigonometry",
            "diff": "Easy"
        },
        {
            "text": "The principal value of sin⁻¹ x lies in",
            "type": "mcq",
            "options": ["[0, π]", "[-π/2, π/2]", "[-π, π]", "[0, 2π]"],
            "correct": "[-π/2, π/2]",
            "cat": "Inv. Trigonometry",
            "diff": "Easy"
        },
        {
            "text": "If x ∈ [-1,1], then cos⁻¹ x lies in",
            "type": "mcq",
            "options": ["[-π, π]", "[0, π]", "[-π/2, π/2]", "[0, 2π]"],
            "correct": "[0, π]",
            "cat": "Inv. Trigonometry",
            "diff": "Easy"
        },

        # --- NEW QUESTIONS ---
        # Unit 1 - App of Matrices (New)
        {
            "text": "If A = [1 2; 3 4], then |adj(A)| =",
            "type": "mcq",
            "options": ["10", "-2", "4", "2"],
            "correct": "-2",
            "cat": "App of Matrices",
            "diff": "Easy"
        },
        {
            "text": "If A is non-singular, then A⁻¹ exists if and only if",
            "type": "mcq",
            "options": ["|A| = 0", "adj(A) = 0", "|A| ≠ 0", "A is symmetric"],
            "correct": "|A| ≠ 0",
            "cat": "App of Matrices",
            "diff": "Easy"
        },
        {
            "text": "If A² = A, then A is called",
            "type": "mcq",
            "options": ["Singular matrix", "Idempotent matrix", "Symmetric matrix", "Skew-symmetric matrix"],
            "correct": "Idempotent matrix",
            "cat": "App of Matrices",
            "diff": "Medium"
        },
        {
            "text": "If A is a singular matrix, then",
            "type": "mcq",
            "options": ["adj(A) exists", "A⁻¹ exists", "|A| ≠ 0", "rank(A) = order(A)"],
            "correct": "adj(A) exists",
            "cat": "App of Matrices",
            "diff": "Medium"
        },
        {
            "text": "If A is square matrix of order 3, then order of adj(A) is",
            "type": "mcq",
            "options": ["2 × 2", "3 × 3", "1 × 3", "3 × 1"],
            "correct": "3 × 3",
            "cat": "App of Matrices",
            "diff": "Easy"
        },
        {
            "text": "If A is square matrix of order n, then A · adj(A) =",
            "type": "mcq",
            "options": ["0", "adj(A)", "|A|Iₙ", "Iₙ"],
            "correct": "|A|Iₙ",
            "cat": "App of Matrices",
            "diff": "Medium"
        },
        {
            "text": "If A is non-singular, then which is true?",
            "type": "mcq",
            "options": ["|A| = 0", "A⁻¹ does not exist", "rank(A) = order(A)", "adj(A) = 0"],
            "correct": "rank(A) = order(A)",
            "cat": "App of Matrices",
            "diff": "Medium"
        },

        # Unit 2 - Complex Numbers (New)
        {
            "text": "If z = 3 - 4i, then |z| =",
            "type": "mcq",
            "options": ["5", "7", "√7", "25"],
            "correct": "5",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        {
            "text": "If z·z̄ = 16, then |z| =",
            "type": "mcq",
            "options": ["4", "-4", "8", "√16"],
            "correct": "4",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        {
            "text": "The modulus of (1-i)/(1+i) is",
            "type": "mcq",
            "options": ["0", "1", "√2", "2"],
            "correct": "1",
            "cat": "Complex Numbers",
            "diff": "Medium"
        },
        {
            "text": "If z = cos θ + i sin θ, then z·z̄ =",
            "type": "mcq",
            "options": ["0", "i", "1", "-1"],
            "correct": "1",
            "cat": "Complex Numbers",
            "diff": "Medium"
        },
        {
            "text": "The argument of a negative real number is",
            "type": "mcq",
            "options": ["0", "π", "π/2", "-π/2"],
            "correct": "π",
            "cat": "Complex Numbers",
            "diff": "Easy"
        },
        {
            "text": "If z is a complex number, then |z|² =",
            "type": "mcq",
            "options": ["z²", "z̄²", "z·z̄", "z + z̄"],
            "correct": "z·z̄",
            "cat": "Complex Numbers",
            "diff": "Medium"
        },

        # Unit 3 - Theory of Equations (New)
        {
            "text": "If coefficients are real and one root is 2 + i, then another root is",
            "type": "mcq",
            "options": ["2 - i", "-2 + i", "-2 - i", "1 - i"],
            "correct": "2 - i",
            "cat": "Theory of Equations",
            "diff": "Easy"
        },
        {
            "text": "The sum of the roots of x³ - 5x² + 6x - 2 = 0 is",
            "type": "mcq",
            "options": ["2", "5", "-5", "6"],
            "correct": "5",
            "cat": "Theory of Equations",
            "diff": "Medium"
        },
        {
            "text": "If all roots of cubic equation are real and distinct, then discriminant is",
            "type": "mcq",
            "options": ["Zero", "Negative", "Positive", "Imaginary"],
            "correct": "Positive",
            "cat": "Theory of Equations",
            "diff": "Hard"
        },
        {
            "text": "Descartes’ rule of signs gives information about",
            "type": "mcq",
            "options": ["Total number of roots", "Imaginary roots", "Positive and negative real roots", "Equal roots"],
            "correct": "Positive and negative real roots",
            "cat": "Theory of Equations",
            "diff": "Medium"
        },
        {
            "text": "If coefficients are real, then non-real roots occur in",
            "type": "mcq",
            "options": ["equal roots", "irrational roots", "conjugate pairs", "negative roots"],
            "correct": "conjugate pairs",
            "cat": "Theory of Equations",
            "diff": "Easy"
        },

        # Unit 4 - Inv. Trigonometry (New)
        {
            "text": "The principal value range of tan⁻¹ x is",
            "type": "mcq",
            "options": ["[0, π]", "(-π/2, π/2)", "[-π, π]", "(0, π)"],
            "correct": "(-π/2, π/2)",
            "cat": "Inv. Trigonometry",
            "diff": "Easy"
        },
        {
            "text": "If x ∈ [-1, 1], then range of sin⁻¹ x is",
            "type": "mcq",
            "options": ["[0, π]", "[-π/2, π/2]", "[-π, π]", "[0, 2π]"],
            "correct": "[-π/2, π/2]",
            "cat": "Inv. Trigonometry",
            "diff": "Easy"
        },
        {
            "text": "cos⁻¹(0) =",
            "type": "mcq",
            "options": ["0", "π", "π/2", "-π/2"],
            "correct": "π/2",
            "cat": "Inv. Trigonometry",
            "diff": "Easy"
        },
        {
            "text": "The principal value of cos⁻¹(-1) is",
            "type": "mcq",
            "options": ["0", "π", "π/2", "-π"],
            "correct": "π",
            "cat": "Inv. Trigonometry",
            "diff": "Medium"
        }
    ]

    print(f"Adding {len(questions_list)} questions...")
    for q in questions_list:
        cursor.execute(
            "INSERT INTO questions (text, type, options, correct_answer, category, difficulty) VALUES (?, ?, ?, ?, ?, ?)",
            (q['text'], q['type'], json.dumps(q['options']), q['correct'], q['cat'], q['diff'])
        )

    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == '__main__':
    seed()
