import json
import datetime
import os
from werkzeug.security import generate_password_hash
from extensions import db
from models import User, Test, Question, Result

def seed_db():
    print("Seeding database...")
    db.create_all()

    # ADMIN
    if not User.query.filter_by(username='elangoadmin').first():
        hash_pw = generate_password_hash('elangoadmin123')
        admin = User(username='elangoadmin', password=hash_pw, role='admin')
        db.session.add(admin)
        print("Admin user created.")

    # STUDENT
    if not User.query.filter_by(username='student').first():
        hash_pw = generate_password_hash('student123')
        student = User(username='student', password=hash_pw, role='student')
        db.session.add(student)
        print("Student user created.")

    # Lathika16
    if not User.query.filter_by(username='Lathika16').first():
        hash_pw = generate_password_hash('Lathika16')
        lathika = User(username='Lathika16', password=hash_pw, role='student')
        db.session.add(lathika)
        print("Lathika16 user created.")

    # Sharuhasan
    if not User.query.filter_by(username='Sharuhasan').first():
        hash_pw = generate_password_hash('Sharuhasan29')
        sharu = User(username='Sharuhasan', password=hash_pw, role='student')
        db.session.add(sharu)
        print("Sharuhasan user created.")

    # RESET DATA - DISABLED to prevent data loss on restart
    # db.session.query(Result).delete()
    # db.session.query(Question).delete()
    # db.session.query(Test).delete()
    # db.session.commit() 
    
    # Only create tests/questions if they don't exist
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    
    # Rename old tests if they exist (Migration)
    old_to_new = {
        "Physics Part 1 (Units 1-4)": "Physics Phase 1 (Units 1-4)",
        "Physics Phase 3 (Units 5-8)": "Physics Phase 2 (Units 5-8)"
    }
    for old, new in old_to_new.items():
        t = Test.query.filter_by(title=old).first()
        if t:
            t.title = new
            db.session.commit()
            print(f"Renamed Test: {old} -> {new}")

    tests_data = [
        ("Maths Phase 1 (Units 1-4)", "Topics: Matrices, Complex Numbers, Theory of Eq, Inv. Trig", yesterday),
        ("Maths Phase 2 (Units 5-8)", "Topics: Two Dimensional Analytical Geometry – II, Applications of Vector Algebra, Applications of Differential Calculus, Differentials and Partial Derivatives", today),
        ("Maths Phase 3 (Units 9-12)", "Topics: Applications of Integration,Ordinary Differential Equations,Probability Distributions,Discrete Mathematics", today),
        ("Physics Phase 1 (Units 1-4)", "Topics: Electrostatics, Current Electricity, Magnetism, EMI & AC", today),
        ("Physics Phase 2 (Units 5-8)", "Topics: EM Waves, Ray Optics, Wave Optics, Dual Nature", tomorrow)
    ]
    
    test_ids = []
    for title, desc, dt in tests_data:
        t = Test.query.filter_by(title=title).first()
        if not t:
            t = Test(title=title, description=desc, scheduled_date=dt)
            db.session.add(t)
            db.session.commit()
            print(f"Created Test: {title}")
        else:
            # Update date if exists (Fix for hosting date mismatch)
            t.scheduled_date = dt
            db.session.commit()
            print(f"Updated Test Date: {title} -> {dt}")
        test_ids.append(t.id)
    
    print(f"Processed {len(test_ids)} tests.")

    # QUESTIONS (Units 5-8 + Book Inside)
    questions_list = [
        # UNIT 5 - 2D Analytical Geometry II
        {"text": "The eccentricity of a circle is", "type": "mcq", "options": ["0", "1", "< 1", "> 1"], "correct": "0", "cat": "2D Analytical Geo", "diff": "Easy", "test_idx": 1},
        {"text": "The centre of the circle x² + y² + 4x - 6y + 9 = 0 is", "type": "mcq", "options": ["(-2, 3)", "(2, -3)", "(-4, 6)", "(4, -6)"], "correct": "(-2, 3)", "cat": "2D Analytical Geo", "diff": "Medium", "test_idx": 1},
        {"text": "The equation of the director circle of x² + y² = a² is", "type": "mcq", "options": ["x² + y² = a²", "x² + y² = 2a²", "x² + y² = 4a²", "x² + y² = 0"], "correct": "x² + y² = 2a²", "cat": "2D Analytical Geo", "diff": "Medium", "test_idx": 1},
        {"text": "The eccentricity of the parabola is", "type": "mcq", "options": ["0", "1", "2", "∞"], "correct": "1", "cat": "2D Analytical Geo", "diff": "Easy", "test_idx": 1},
        {"text": "The latus rectum of the parabola y² = 4ax is", "type": "mcq", "options": ["a", "2a", "4a", "8a"], "correct": "4a", "cat": "2D Analytical Geo", "diff": "Easy", "test_idx": 1},
        {"text": "The focus of the parabola x² = 4ay is", "type": "mcq", "options": ["(a,0)", "(0,a)", "(-a,0)", "(0,-a)"], "correct": "(0,a)", "cat": "2D Analytical Geo", "diff": "Medium", "test_idx": 1},
        {"text": "The equation of the tangent to x² + y² = a² at (x₁, y₁) is", "type": "mcq", "options": ["xx₁ + yy₁ = a²", "xx₁ + yy₁ = 0", "x² + y² = a²", "x₁² + y₁² = a²"], "correct": "xx₁ + yy₁ = a²", "cat": "2D Analytical Geo", "diff": "Medium", "test_idx": 1},
        {"text": "The eccentricity of an ellipse is", "type": "mcq", "options": ["> 1", "= 1", "< 1", "= 0"], "correct": "< 1", "cat": "2D Analytical Geo", "diff": "Easy", "test_idx": 1},
        {"text": "The length of major axis of ellipse x²/a² + y²/b² = 1 is", "type": "mcq", "options": ["a", "2a", "b", "2b"], "correct": "2a", "cat": "2D Analytical Geo", "diff": "Easy", "test_idx": 1},
        {"text": "The condition for tangency of y = mx + c to x² + y² = a² is", "type": "mcq", "options": ["c² = a²", "c² = a²(1 + m²)", "m² = a²", "c = a"], "correct": "c² = a²(1 + m²)", "cat": "2D Analytical Geo", "diff": "Hard", "test_idx": 1},
        {"text": "The eccentricity of a hyperbola is", "type": "mcq", "options": ["< 1", "= 1", "> 1", "= 0"], "correct": "> 1", "cat": "2D Analytical Geo", "diff": "Easy", "test_idx": 1},
        {"text": "The transverse axis of x²/a² - y²/b² = 1 lies along", "type": "mcq", "options": ["x-axis", "y-axis", "origin", "y = x"], "correct": "x-axis", "cat": "2D Analytical Geo", "diff": "Medium", "test_idx": 1},

        # UNIT 6 - Applications of Vector Algebra (11 Questions)
        {"text": "If a · b = 0, then the vectors are", "type": "mcq", "options": ["parallel", "equal", "perpendicular", "collinear"], "correct": "perpendicular", "cat": "Vector Algebra", "diff": "Easy", "test_idx": 1},
        {"text": "The magnitude of i + j is", "type": "mcq", "options": ["1", "√2", "2", "√3"], "correct": "√2", "cat": "Vector Algebra", "diff": "Easy", "test_idx": 1},
        {"text": "The scalar triple product represents", "type": "mcq", "options": ["area", "volume", "length", "angle"], "correct": "volume", "cat": "Vector Algebra", "diff": "Medium", "test_idx": 1},
        {"text": "If [a b c] = 0, then the vectors are", "type": "mcq", "options": ["collinear", "coplanar", "perpendicular", "equal"], "correct": "coplanar", "cat": "Vector Algebra", "diff": "Medium", "test_idx": 1},
        {"text": "a × b is perpendicular to", "type": "mcq", "options": ["a", "b", "both a and b", "none"], "correct": "both a and b", "cat": "Vector Algebra", "diff": "Easy", "test_idx": 1},
        {"text": "The unit vector along x-axis is", "type": "mcq", "options": ["j", "k", "i", "-i"], "correct": "i", "cat": "Vector Algebra", "diff": "Easy", "test_idx": 1},
        {"text": "If a and b are parallel, then", "type": "mcq", "options": ["a · b = 0", "a × b = 0", "|a| = |b|", "angle = 90°"], "correct": "a × b = 0", "cat": "Vector Algebra", "diff": "Easy", "test_idx": 1},
        {"text": "The vector product is also called", "type": "mcq", "options": ["scalar product", "dot product", "cross product", "triple product"], "correct": "cross product", "cat": "Vector Algebra", "diff": "Easy", "test_idx": 1},
        {"text": "The angle between identical vectors is", "type": "mcq", "options": ["0°", "45°", "90°", "180°"], "correct": "0°", "cat": "Vector Algebra", "diff": "Easy", "test_idx": 1},
        {"text": "The direction ratios of x-axis are", "type": "mcq", "options": ["(0,1,0)", "(1,0,0)", "(0,0,1)", "(1,1,0)"], "correct": "(1,0,0)", "cat": "Vector Algebra", "diff": "Easy", "test_idx": 1},
        {"text": "The volume of parallelepiped formed by coplanar vectors is", "type": "mcq", "options": ["1", "maximum", "minimum", "zero"], "correct": "zero", "cat": "Vector Algebra", "diff": "Medium", "test_idx": 1},

        # UNIT 7 - Applications of Differential Calculus (11 Questions)
        {"text": "The derivative represents", "type": "mcq", "options": ["area", "slope", "volume", "length"], "correct": "slope", "cat": "Diff Calculus", "diff": "Easy", "test_idx": 1},
        {"text": "If f'(x) > 0, then f(x) is", "type": "mcq", "options": ["decreasing", "constant", "increasing", "discontinuous"], "correct": "increasing", "cat": "Diff Calculus", "diff": "Easy", "test_idx": 1},
        {"text": "At maximum point", "type": "mcq", "options": ["f'(x) > 0", "f'(x) < 0", "f'(x) = 0", "f''(x) = 0"], "correct": "f'(x) = 0", "cat": "Diff Calculus", "diff": "Medium", "test_idx": 1},
        {"text": "Rolle’s theorem requires", "type": "mcq", "options": ["continuity", "differentiability", "equal end values", "all the above"], "correct": "all the above", "cat": "Diff Calculus", "diff": "Medium", "test_idx": 1},
        {"text": "The slope of the tangent is", "type": "mcq", "options": ["f(x)", "f'(x)", "f''(x)", "∫f(x)dx"], "correct": "f'(x)", "cat": "Diff Calculus", "diff": "Easy", "test_idx": 1},
        {"text": "The point where f''(x) = 0 is called", "type": "mcq", "options": ["maximum", "minimum", "inflection", "asymptote"], "correct": "inflection", "cat": "Diff Calculus", "diff": "Medium", "test_idx": 1},
        {"text": "Velocity is the rate of change of", "type": "mcq", "options": ["distance", "displacement", "speed", "acceleration"], "correct": "displacement", "cat": "Diff Calculus", "diff": "Easy", "test_idx": 1},
        {"text": "Acceleration is", "type": "mcq", "options": ["ds/dt", "dv/dt", "dx/dt", "dt/dx"], "correct": "dv/dt", "cat": "Diff Calculus", "diff": "Easy", "test_idx": 1},
        {"text": "The curve is concave upward if", "type": "mcq", "options": ["f''(x) < 0", "f''(x) = 0", "f''(x) > 0", "f'(x) = 0"], "correct": "f''(x) > 0", "cat": "Diff Calculus", "diff": "Medium", "test_idx": 1},
        {"text": "The average rate of change is", "type": "mcq", "options": ["derivative", "limit", "difference quotient", "integral"], "correct": "difference quotient", "cat": "Diff Calculus", "diff": "Hard", "test_idx": 1},
        {"text": "The tangent at a point is horizontal if", "type": "mcq", "options": ["f(x) = 0", "f'(x) = 0", "f''(x) = 0", "x = 0"], "correct": "f'(x) = 0", "cat": "Diff Calculus", "diff": "Easy", "test_idx": 1},

        # UNIT 8 - Differentials & Partial Derivatives (11 Questions)
        {"text": "The differential of x^n is", "type": "mcq", "options": ["nx^(n-1)", "nx^(n-1)dx", "x^ndx", "ndx"], "correct": "nx^(n-1)dx", "cat": "Part Derivatives", "diff": "Medium", "test_idx": 1},
        {"text": "Partial derivatives are used when the function has", "type": "mcq", "options": ["one variable", "two or more variables", "constants only", "no variables"], "correct": "two or more variables", "cat": "Part Derivatives", "diff": "Easy", "test_idx": 1},
        {"text": "∂y/∂x equals", "type": "mcq", "options": ["0", "1", "x", "y"], "correct": "0", "cat": "Part Derivatives", "diff": "Easy", "test_idx": 1},
        {"text": "If z = x² + y², then ∂z/∂x is", "type": "mcq", "options": ["2y", "2x", "x", "y"], "correct": "2x", "cat": "Part Derivatives", "diff": "Easy", "test_idx": 1},
        {"text": "Total differential involves", "type": "mcq", "options": ["one variable", "two variables", "constants", "integration"], "correct": "two variables", "cat": "Part Derivatives", "diff": "Medium", "test_idx": 1},
        {"text": "If y = f(x), then dy/dx is called", "type": "mcq", "options": ["integral", "limit", "derivative", "differential equation"], "correct": "derivative", "cat": "Part Derivatives", "diff": "Easy", "test_idx": 1},
        {"text": "The differential gives", "type": "mcq", "options": ["exact value", "approximate change", "area", "volume"], "correct": "approximate change", "cat": "Part Derivatives", "diff": "Medium", "test_idx": 1},
        {"text": "A function of two variables is written as", "type": "mcq", "options": ["y = f(x)", "z = f(x,y)", "x = f(y)", "y = f(z)"], "correct": "z = f(x,y)", "cat": "Part Derivatives", "diff": "Easy", "test_idx": 1},
        {"text": "The symbol ∂ is used for", "type": "mcq", "options": ["derivative", "integration", "partial derivative", "limit"], "correct": "partial derivative", "cat": "Part Derivatives", "diff": "Easy", "test_idx": 1},
        {"text": "Linear approximation uses", "type": "mcq", "options": ["first derivative", "second derivative", "integral", "limit"], "correct": "first derivative", "cat": "Part Derivatives", "diff": "Medium", "test_idx": 1},
        {"text": "If z = x + y, then ∂z/∂y is", "type": "mcq", "options": ["x", "y", "1", "0"], "correct": "1", "cat": "Part Derivatives", "diff": "Easy", "test_idx": 1},

        # PART B: BOOK INSIDE QUESTIONS (15 MCQs)
        {"text": "The eccentricity measures the", "type": "mcq", "options": ["size of conic", "shape of conic", "area", "volume"], "correct": "shape of conic", "cat": "Book Inside", "diff": "Medium", "test_idx": 1},
        {"text": "The dot product gives a", "type": "mcq", "options": ["vector", "scalar", "matrix", "point"], "correct": "scalar", "cat": "Book Inside", "diff": "Easy", "test_idx": 1},
        {"text": "Coplanar vectors lie in", "type": "mcq", "options": ["line", "plane", "space", "axis"], "correct": "plane", "cat": "Book Inside", "diff": "Easy", "test_idx": 1},
        {"text": "The derivative is defined as a", "type": "mcq", "options": ["limit", "sum", "product", "quotient"], "correct": "limit", "cat": "Book Inside", "diff": "Medium", "test_idx": 1},
        {"text": "If slope is zero, the line is", "type": "mcq", "options": ["vertical", "horizontal", "inclined", "parallel to y-axis"], "correct": "horizontal", "cat": "Book Inside", "diff": "Easy", "test_idx": 1},
        {"text": "Differentiation is the inverse of", "type": "mcq", "options": ["subtraction", "multiplication", "integration", "division"], "correct": "integration", "cat": "Book Inside", "diff": "Medium", "test_idx": 1},
        {"text": "The partial derivative treats other variables as", "type": "mcq", "options": ["zero", "constant", "variable", "function"], "correct": "constant", "cat": "Book Inside", "diff": "Medium", "test_idx": 1},
        {"text": "The second derivative gives information about", "type": "mcq", "options": ["slope", "curvature", "area", "length"], "correct": "curvature", "cat": "Book Inside", "diff": "Hard", "test_idx": 1},
        {"text": "The rate of change of distance is", "type": "mcq", "options": ["acceleration", "velocity", "speed", "force"], "correct": "velocity", "cat": "Book Inside", "diff": "Easy", "test_idx": 1},
        {"text": "The focus is a concept related to", "type": "mcq", "options": ["vectors", "calculus", "conics", "matrices"], "correct": "conics", "cat": "Book Inside", "diff": "Easy", "test_idx": 1},
        {"text": "The gradient of a curve at a point is", "type": "mcq", "options": ["y", "x", "dy/dx", "dx/dy"], "correct": "dy/dx", "cat": "Book Inside", "diff": "Medium", "test_idx": 1},
        {"text": "The symbol ∆ represents", "type": "mcq", "options": ["partial change", "limit", "total change", "derivative"], "correct": "total change", "cat": "Book Inside", "diff": "Easy", "test_idx": 1},
        {"text": "The tangent touches the curve at", "type": "mcq", "options": ["one point", "two points", "many points", "no point"], "correct": "one point", "cat": "Book Inside", "diff": "Easy", "test_idx": 1},
        {"text": "The scalar triple product is zero for", "type": "mcq", "options": ["parallel vectors", "coplanar vectors", "perpendicular vectors", "unit vectors"], "correct": "coplanar vectors", "cat": "Book Inside", "diff": "Medium", "test_idx": 1},
        {"text": "Linear approximation is useful for", "type": "mcq", "options": ["exact values", "rough values", "integration", "limits"], "correct": "rough values", "cat": "Book Inside", "diff": "Easy", "test_idx": 1},
        
        # UNIT 9-12 (Phase 3) - 60 Questions
        # Easy
        {"text": "The integral of x is", "type": "mcq", "options": ["x", "x²", "x²/2", "ln x"], "correct": "x²/2", "cat": "Integration", "diff": "Easy", "test_idx": 2},
        {"text": "The order of the differential equation dy/dx = x is", "type": "mcq", "options": ["0", "1", "2", "3"], "correct": "1", "cat": "Diff Equations", "diff": "Easy", "test_idx": 2},
        {"text": "The probability of a sure event is", "type": "mcq", "options": ["0", "-1", "1", "∞"], "correct": "1", "cat": "Probability", "diff": "Easy", "test_idx": 2},
        {"text": "A statement which is either true or false is called", "type": "mcq", "options": ["sentence", "proposition", "equation", "variable"], "correct": "proposition", "cat": "Discrete Math", "diff": "Easy", "test_idx": 2},
        {"text": "The symbol used for integration is", "type": "mcq", "options": ["∂", "Δ", "∫", "Σ"], "correct": "∫", "cat": "Integration", "diff": "Easy", "test_idx": 2},
        {"text": "The degree of (dy/dx)² = x is", "type": "mcq", "options": ["1", "2", "0", "not defined"], "correct": "2", "cat": "Diff Equations", "diff": "Easy", "test_idx": 2},
        {"text": "The mean of a probability distribution is also called", "type": "mcq", "options": ["variance", "expectation", "standard deviation", "mode"], "correct": "expectation", "cat": "Probability", "diff": "Easy", "test_idx": 2},
        {"text": "The negation of the statement p is", "type": "mcq", "options": ["p", "¬p", "p ∧ q", "p ∨ q"], "correct": "¬p", "cat": "Discrete Math", "diff": "Easy", "test_idx": 2},
        {"text": "The area under a curve is found by", "type": "mcq", "options": ["differentiation", "integration", "limits", "matrices"], "correct": "integration", "cat": "Integration", "diff": "Easy", "test_idx": 2},
        {"text": "A random variable takes", "type": "mcq", "options": ["letters", "symbols", "numerical values", "words"], "correct": "numerical values", "cat": "Probability", "diff": "Easy", "test_idx": 2},

        # Medium
        {"text": "∫(0 to 1) x² dx =", "type": "mcq", "options": ["1", "1/2", "1/3", "2"], "correct": "1/3", "cat": "Integration", "diff": "Medium", "test_idx": 2},
        {"text": "Area bounded by y=x, x-axis and x=2 is", "type": "mcq", "options": ["1", "2", "4", "3"], "correct": "2", "cat": "Integration", "diff": "Medium", "test_idx": 2},
        {"text": "The volume obtained by revolving about x-axis is found using", "type": "mcq", "options": ["shell method", "disk method", "trapezium rule", "Simpson’s rule"], "correct": "disk method", "cat": "Integration", "diff": "Medium", "test_idx": 2},
        {"text": "∫ e^x dx equals", "type": "mcq", "options": ["xe^x", "e^x + C", "e^x + 1", "ln x"], "correct": "e^x + C", "cat": "Integration", "diff": "Medium", "test_idx": 2},
        {"text": "∫ cos x dx =", "type": "mcq", "options": ["sin x + C", "-sin x + C", "tan x + C", "-cos x + C"], "correct": "sin x + C", "cat": "Integration", "diff": "Medium", "test_idx": 2},
        {"text": "The order of d²y/dx² + dy/dx = 0 is", "type": "mcq", "options": ["1", "2", "3", "0"], "correct": "2", "cat": "Diff Equations", "diff": "Medium", "test_idx": 2},
        {"text": "The degree of (d²y/dx²)³ = x is", "type": "mcq", "options": ["1", "2", "3", "0"], "correct": "3", "cat": "Diff Equations", "diff": "Medium", "test_idx": 2},
        {"text": "The general solution of dy/dx = 0 is", "type": "mcq", "options": ["y = 0", "y = x", "y = c", "y = eˣ"], "correct": "y = c", "cat": "Diff Equations", "diff": "Medium", "test_idx": 2},
        {"text": "A differential equation containing only y and dy/dx is", "type": "mcq", "options": ["linear", "separable", "exact", "non-linear"], "correct": "separable", "cat": "Diff Equations", "diff": "Medium", "test_idx": 2},
        {"text": "The solution of dy/dx = y is", "type": "mcq", "options": ["y = x + C", "y = Ce^x", "y = Cx", "y = ln x"], "correct": "y = Ce^x", "cat": "Diff Equations", "diff": "Medium", "test_idx": 2},
        {"text": "If A and B are mutually exclusive, then", "type": "mcq", "options": ["P(A∩B)=1", "P(A∪B)=0", "P(A∩B)=0", "P(A)=P(B)"], "correct": "P(A∩B)=0", "cat": "Probability", "diff": "Medium", "test_idx": 2},
        {"text": "Mean of binomial distribution is", "type": "mcq", "options": ["nq", "np", "pq", "n"], "correct": "np", "cat": "Probability", "diff": "Medium", "test_idx": 2},
        {"text": "Variance of binomial distribution is", "type": "mcq", "options": ["np", "npq", "nq", "pq"], "correct": "npq", "cat": "Probability", "diff": "Medium", "test_idx": 2},
        {"text": "If P(A)=0.4, then P(A′)=", "type": "mcq", "options": ["0.6", "0.4", "1.4", "0"], "correct": "0.6", "cat": "Probability", "diff": "Medium", "test_idx": 2},
        {"text": "A fair coin is tossed. Probability of getting a head is", "type": "mcq", "options": ["0", "1", "1/2", "2"], "correct": "1/2", "cat": "Probability", "diff": "Medium", "test_idx": 2},
        {"text": "The truth value of p ∨ q is false when", "type": "mcq", "options": ["p is true", "q is true", "both are false", "both are true"], "correct": "both are false", "cat": "Discrete Math", "diff": "Medium", "test_idx": 2},
        {"text": "The negation of p ∧ q is", "type": "mcq", "options": ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∨ q", "p ∧ q"], "correct": "¬p ∨ ¬q", "cat": "Discrete Math", "diff": "Medium", "test_idx": 2},
        {"text": "Converse of 'If p then q' is", "type": "mcq", "options": ["If q then p", "If ¬p then ¬q", "p ∧ q", "p ∨ q"], "correct": "If q then p", "cat": "Discrete Math", "diff": "Medium", "test_idx": 2},
        {"text": "A binary operation on a set maps", "type": "mcq", "options": ["S → S", "S × S → S", "S → S × S", "S × S → R"], "correct": "S × S → S", "cat": "Discrete Math", "diff": "Medium", "test_idx": 2},
        {"text": "The statement p → q is false when", "type": "mcq", "options": ["p true, q true", "p false, q true", "p false, q false", "p true, q false"], "correct": "p true, q false", "cat": "Discrete Math", "diff": "Medium", "test_idx": 2},

        # Hard
        {"text": "Area between curves y=x and y=x² in [0,1] is", "type": "mcq", "options": ["1/2", "1/3", "1/6", "2/3"], "correct": "1/6", "cat": "Integration", "diff": "Hard", "test_idx": 2},
        {"text": "The solution of dy/dx + y = 0 is", "type": "mcq", "options": ["y = Ce^x", "y = Ce^-x", "y = Cx", "y = 0"], "correct": "y = Ce^-x", "cat": "Diff Equations", "diff": "Hard", "test_idx": 2},
        {"text": "If X is a random variable with values 1,2,3 each having probability 1/3, then mean is", "type": "mcq", "options": ["1", "2", "3", "4"], "correct": "2", "cat": "Probability", "diff": "Hard", "test_idx": 2},
        {"text": "The negation of (p → q) is", "type": "mcq", "options": ["p → ¬q", "¬p → q", "p ∧ ¬q", "¬p ∧ q"], "correct": "p ∧ ¬q", "cat": "Discrete Math", "diff": "Hard", "test_idx": 2},
        {"text": "If P(A)=1, then A is a", "type": "mcq", "options": ["impossible event", "random event", "sure event", "equally likely event"], "correct": "sure event", "cat": "Probability", "diff": "Hard", "test_idx": 2},
        {"text": "Degree of dy/dx + y = 0 is", "type": "mcq", "options": ["1", "2", "0", "not defined"], "correct": "not defined", "cat": "Diff Equations", "diff": "Hard", "test_idx": 2},
        {"text": "The expectation of a constant k is", "type": "mcq", "options": ["0", "1", "k", "k²"], "correct": "k", "cat": "Probability", "diff": "Hard", "test_idx": 2},
        {"text": "The contrapositive of p → q is", "type": "mcq", "options": ["¬q → ¬p", "q → p", "¬p → ¬q", "p → ¬q"], "correct": "¬q → ¬p", "cat": "Discrete Math", "diff": "Hard", "test_idx": 2},
        {"text": "If two events are independent, then", "type": "mcq", "options": ["P(A∩B)=0", "P(A∩B)=P(A)+P(B)", "P(A∩B)=P(A)P(B)", "P(A)=P(B)"], "correct": "P(A∩B)=P(A)P(B)", "cat": "Probability", "diff": "Hard", "test_idx": 2},
        {"text": "The volume generated by revolving y=f(x) about y-axis uses", "type": "mcq", "options": ["disk method", "shell method", "Simpson rule", "trapezium rule"], "correct": "shell method", "cat": "Integration", "diff": "Hard", "test_idx": 2},

        # Additional Medium
        {"text": "The area bounded by the curve y=x², x-axis and x = 2 is", "type": "mcq", "options": ["8/3", "4/3", "4", "2"], "correct": "8/3", "cat": "Integration", "diff": "Medium", "test_idx": 2},
        {"text": "The integral ∫(0 to 2) 3x² dx is", "type": "mcq", "options": ["4", "6", "8", "12"], "correct": "12", "cat": "Integration", "diff": "Medium", "test_idx": 2},
        {"text": "The differential equation dy/dx = x² is", "type": "mcq", "options": ["linear", "separable", "homogeneous", "exact"], "correct": "separable", "cat": "Diff Equations", "diff": "Medium", "test_idx": 2},
        {"text": "The solution of dy/dx = 2x is", "type": "mcq", "options": ["y=x² + C", "y=2x + C", "y=x + C", "y=2x² + C"], "correct": "y=x² + C", "cat": "Diff Equations", "diff": "Medium", "test_idx": 2},
        {"text": "If P(A)=0.7, then the probability of not A is", "type": "mcq", "options": ["0.7", "0.3", "1.7", "0"], "correct": "0.3", "cat": "Probability", "diff": "Medium", "test_idx": 2},
        {"text": "The sum of probabilities of all possible outcomes of a random experiment is", "type": "mcq", "options": ["0", "less than 1", "greater than 1", "1"], "correct": "1", "cat": "Probability", "diff": "Medium", "test_idx": 2},
        {"text": "The truth value of the statement p ∧ q is true when", "type": "mcq", "options": ["p is true", "q is true", "both p and q are true", "both p and q are false"], "correct": "both p and q are true", "cat": "Discrete Math", "diff": "Medium", "test_idx": 2},
        {"text": "If p is false and q is true, then p → q is", "type": "mcq", "options": ["true", "false", "undefined", "depends on p"], "correct": "true", "cat": "Discrete Math", "diff": "Medium", "test_idx": 2},
        {"text": "Mean of probability distribution x:1,2,3 P(x):1/3,1/3,1/3 is", "type": "mcq", "options": ["1", "2", "3", "4"], "correct": "2", "cat": "Probability", "diff": "Medium", "test_idx": 2},
        {"text": "The solution of dy/dx + 2y = 0 is", "type": "mcq", "options": ["y = Ce^2x", "y = Ce^-2x", "y = 2Ce^x", "y = Cx^-2"], "correct": "y = Ce^-2x", "cat": "Diff Equations", "diff": "Medium", "test_idx": 2},
        
        # Additional Hard
        {"text": "The area enclosed between the curves y=x and y=x³ in [0,1] is", "type": "mcq", "options": ["1/2", "1/4", "1/6", "1/12"], "correct": "1/12", "cat": "Integration", "diff": "Hard", "test_idx": 2},
        {"text": "Volume by revolving y=x from x=0 to 1 about y-axis is", "type": "mcq", "options": ["1/2", "1/3", "1/4", "1/6"], "correct": "1/3", "cat": "Integration", "diff": "Hard", "test_idx": 2},
        {"text": "Order of (d³y/dx³)² + y = 0 is", "type": "mcq", "options": ["1", "2", "3", "6"], "correct": "3", "cat": "Diff Equations", "diff": "Hard", "test_idx": 2},
        {"text": "Degree of (dy/dx)³ + y = 0 is", "type": "mcq", "options": ["1", "2", "3", "not defined"], "correct": "3", "cat": "Diff Equations", "diff": "Hard", "test_idx": 2},
        {"text": "If X is a random variable with mean 5, then E(X − 2) is", "type": "mcq", "options": ["2", "3", "5", "7"], "correct": "3", "cat": "Probability", "diff": "Hard", "test_idx": 2},
        {"text": "If two events A and B are independent, then P(A∣B) =", "type": "mcq", "options": ["P(A+B)", "P(A)", "P(B)", "0"], "correct": "P(A)", "cat": "Probability", "diff": "Hard", "test_idx": 2},
        {"text": "Negation of 'p or q' is", "type": "mcq", "options": ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∧ q", "p → q"], "correct": "¬p ∧ ¬q", "cat": "Discrete Math", "diff": "Hard", "test_idx": 2},
        {"text": "Contrapositive of 'If p then q' is", "type": "mcq", "options": ["If q then p", "If ¬p then ¬q", "If ¬q then ¬p", "If p then ¬q"], "correct": "If ¬q then ¬p", "cat": "Discrete Math", "diff": "Hard", "test_idx": 2},
        {"text": "If P(A)=0.4, P(B)=0.5 and independent, then P(A ∩ B) is", "type": "mcq", "options": ["0.9", "0.2", "0.45", "0.1"], "correct": "0.2", "cat": "Probability", "diff": "Hard", "test_idx": 2},
        {"text": "p ↔ q is true when", "type": "mcq", "options": ["p is true and q is false", "p is false and q is true", "p and q have same truth value", "p and q have different truth values"], "correct": "p and q have same truth value", "cat": "Discrete Math", "diff": "Hard", "test_idx": 2},
        
        # Physics Phase 3 (Units 5-8) - 60 Questions
        # Unit 5 : Electromagnetic Waves
        {"text": "The speed of electromagnetic waves in vacuum is", "type": "mcq", "options": ["c", "v", "c/n", "infinity"], "correct": "c", "cat": "EM Waves", "diff": "Easy", "test_idx": 4},
        {"text": "Electromagnetic waves are", "type": "mcq", "options": ["longitudinal", "transverse", "both", "none"], "correct": "transverse", "cat": "EM Waves", "diff": "Easy", "test_idx": 4},
        {"text": "The oscillating electric and magnetic fields are in phase and perpendicular to each other and to the direction of propagation.", "type": "mcq", "options": ["True", "False", "Sometimes", "Depends on medium"], "correct": "True", "cat": "EM Waves", "diff": "Easy", "test_idx": 4},
        {"text": "Which of the following has the highest frequency?", "type": "mcq", "options": ["Radio waves", "Microwaves", "Gamma rays", "X-rays"], "correct": "Gamma rays", "cat": "EM Waves", "diff": "Medium", "test_idx": 4},
        {"text": "The energy density of electric field in EM wave is", "type": "mcq", "options": ["½ε₀E²", "½μ₀H²", "E/B", "B/E"], "correct": "½ε₀E²", "cat": "EM Waves", "diff": "Medium", "test_idx": 4},
        {"text": "The relation between E and B in EM waves is", "type": "mcq", "options": ["E = cB", "B = cE", "E = B", "E = B/c"], "correct": "E = cB", "cat": "EM Waves", "diff": "Easy", "test_idx": 4},
        {"text": "Maxwell’s equations are based on", "type": "mcq", "options": ["Newton's laws", "Conservation laws", "Electromagnetic principles", "Quantum mechanics"], "correct": "Electromagnetic principles", "cat": "EM Waves", "diff": "Medium", "test_idx": 4},
        {"text": "Displacement current is given by", "type": "mcq", "options": ["I_c", "ε₀ dΦ_E/dt", "μ₀ dΦ_B/dt", "I_d"], "correct": "ε₀ dΦ_E/dt", "cat": "EM Waves", "diff": "Hard", "test_idx": 4},
        {"text": "The source of electromagnetic waves is", "type": "mcq", "options": ["stationary charge", "charge at constant velocity", "accelerated charge", "neutral particle"], "correct": "accelerated charge", "cat": "EM Waves", "diff": "Medium", "test_idx": 4},
        {"text": "Poynting vector represents", "type": "mcq", "options": ["energy flux", "momentum", "force", "power"], "correct": "energy flux", "cat": "EM Waves", "diff": "Hard", "test_idx": 4},
        {"text": "Which part of the EM spectrum is used in remote controls?", "type": "mcq", "options": ["Visible light", "Infrared", "Ultraviolet", "Microwaves"], "correct": "Infrared", "cat": "EM Waves", "diff": "Easy", "test_idx": 4},
        {"text": "Ozone layer absorbs", "type": "mcq", "options": ["Infrared", "Visible light", "Ultraviolet", "Radio waves"], "correct": "Ultraviolet", "cat": "EM Waves", "diff": "Easy", "test_idx": 4},
        {"text": "The wavelength range of visible light is approximately", "type": "mcq", "options": ["100-400 nm", "400-700 nm", "700-1000 nm", "1-10 mm"], "correct": "400-700 nm", "cat": "EM Waves", "diff": "Medium", "test_idx": 4},
        {"text": "Which EM wave is used in MRI?", "type": "mcq", "options": ["X-rays", "Gamma rays", "Radio waves", "Microwaves"], "correct": "Radio waves", "cat": "EM Waves", "diff": "Medium", "test_idx": 4},
        {"text": "The unit of Poynting vector is", "type": "mcq", "options": ["J/s", "W/m²", "N/m", "J m"], "correct": "W/m²", "cat": "EM Waves", "diff": "Hard", "test_idx": 4},

        # Unit 6 : Ray Optics
        {"text": "The phenomenon of light bending when passing from one medium to another is called", "type": "mcq", "options": ["reflection", "refraction", "diffraction", "polarization"], "correct": "refraction", "cat": "Ray Optics", "diff": "Easy", "test_idx": 4},
        {"text": "Snell's law relates", "type": "mcq", "options": ["angle of incidence and reflection", "angle of incidence and refraction", "wavelength and frequency", "speed and wavelength"], "correct": "angle of incidence and refraction", "cat": "Ray Optics", "diff": "Easy", "test_idx": 4},
        {"text": "Total internal reflection occurs when light travels from", "type": "mcq", "options": ["denser to rarer medium", "rarer to denser medium", "air to vacuum", "vacuum to air"], "correct": "denser to rarer medium", "cat": "Ray Optics", "diff": "Easy", "test_idx": 4},
        {"text": "The critical angle depends on", "type": "mcq", "options": ["intensity of light", "color of light", "size of medium", "shape of interface"], "correct": "color of light", "cat": "Ray Optics", "diff": "Medium", "test_idx": 4},
        {"text": "A convex lens is a", "type": "mcq", "options": ["diverging lens", "converging lens", "plane mirror", "prism"], "correct": "converging lens", "cat": "Ray Optics", "diff": "Easy", "test_idx": 4},
        {"text": "The power of a lens is measured in", "type": "mcq", "options": ["meters", "centimeters", "diopters", "watts"], "correct": "diopters", "cat": "Ray Optics", "diff": "Easy", "test_idx": 4},
        {"text": "For a real image formed by a lens, the magnification is", "type": "mcq", "options": ["positive", "negative", "zero", "infinite"], "correct": "negative", "cat": "Ray Optics", "diff": "Medium", "test_idx": 4},
        {"text": "The focal length of a plane mirror is", "type": "mcq", "options": ["zero", "infinity", "positive", "negative"], "correct": "infinity", "cat": "Ray Optics", "diff": "Medium", "test_idx": 4},
        {"text": "Dispersion of light is the phenomenon of", "type": "mcq", "options": ["splitting of light into its constituent colors", "bending of light", "reflection of light", "scattering of light"], "correct": "splitting of light into its constituent colors", "cat": "Ray Optics", "diff": "Easy", "test_idx": 4},
        {"text": "Rainbow formation is due to", "type": "mcq", "options": ["reflection only", "refraction only", "dispersion and total internal reflection", "diffraction only"], "correct": "dispersion and total internal reflection", "cat": "Ray Optics", "diff": "Hard", "test_idx": 4},
        {"text": "Myopia can be corrected by using a", "type": "mcq", "options": ["convex lens", "concave lens", "cylindrical lens", "bifocal lens"], "correct": "concave lens", "cat": "Ray Optics", "diff": "Easy", "test_idx": 4},
        {"text": "Hypermetropia can be corrected by using a", "type": "mcq", "options": ["convex lens", "concave lens", "cylindrical lens", "bifocal lens"], "correct": "convex lens", "cat": "Ray Optics", "diff": "Easy", "test_idx": 4},
        {"text": "The image formed by a simple microscope is", "type": "mcq", "options": ["real and inverted", "virtual and inverted", "real and erect", "virtual and erect"], "correct": "virtual and erect", "cat": "Ray Optics", "diff": "Medium", "test_idx": 4},
        {"text": "The magnifying power of a compound microscope is increased by increasing the focal length of the", "type": "mcq", "options": ["eyepiece", "objective", "both", "none"], "correct": "objective", "cat": "Ray Optics", "diff": "Hard", "test_idx": 4},
        {"text": "The resolving power of a telescope depends on", "type": "mcq", "options": ["focal length of objective", "diameter of objective", "wavelength of light", "both diameter and wavelength"], "correct": "both diameter and wavelength", "cat": "Ray Optics", "diff": "Hard", "test_idx": 4},

        # Unit 7 : Wave Optics
        {"text": "Huygens' principle states that every point on a wavefront is a source of", "type": "mcq", "options": ["light rays", "secondary wavelets", "particles", "energy"], "correct": "secondary wavelets", "cat": "Wave Optics", "diff": "Easy", "test_idx": 4},
        {"text": "Interference of light is the phenomenon of", "type": "mcq", "options": ["redistribution of light energy", "bending of light", "splitting of light", "scattering of light"], "correct": "redistribution of light energy", "cat": "Wave Optics", "diff": "Easy", "test_idx": 4},
        {"text": "For sustained interference, the sources must be", "type": "mcq", "options": ["monochromatic", "coherent", "incoherent", "polychromatic"], "correct": "coherent", "cat": "Wave Optics", "diff": "Easy", "test_idx": 4},
        {"text": "In Young's double-slit experiment, the fringe width is proportional to", "type": "mcq", "options": ["wavelength", "distance between slits", "distance to screen", "all of the above"], "correct": "wavelength", "cat": "Wave Optics", "diff": "Medium", "test_idx": 4},
        {"text": "Diffraction is the phenomenon of", "type": "mcq", "options": ["bending of light around obstacles", "reflection of light", "refraction of light", "polarization of light"], "correct": "bending of light around obstacles", "cat": "Wave Optics", "diff": "Easy", "test_idx": 4},
        {"text": "Fraunhofer diffraction occurs when the source and screen are at", "type": "mcq", "options": ["finite distance", "infinite distance", "close to aperture", "any distance"], "correct": "infinite distance", "cat": "Wave Optics", "diff": "Medium", "test_idx": 4},
        {"text": "Polarization of light proves that light waves are", "type": "mcq", "options": ["longitudinal", "transverse", "stationary", "mechanical"], "correct": "transverse", "cat": "Wave Optics", "diff": "Easy", "test_idx": 4},
        {"text": "Brewster's law relates the polarizing angle to the", "type": "mcq", "options": ["wavelength", "frequency", "refractive index", "intensity"], "correct": "refractive index", "cat": "Wave Optics", "diff": "Medium", "test_idx": 4},
        {"text": "The condition for constructive interference is path difference =", "type": "mcq", "options": ["nλ", "(n+½)λ", "nλ/2", "0"], "correct": "nλ", "cat": "Wave Optics", "diff": "Easy", "test_idx": 4},
        {"text": "The condition for destructive interference is path difference =", "type": "mcq", "options": ["nλ", "(n+½)λ", "nλ/2", "0"], "correct": "(n+½)λ", "cat": "Wave Optics", "diff": "Easy", "test_idx": 4},
        {"text": "The intensity of light in interference pattern is proportional to", "type": "mcq", "options": ["amplitude", "square of amplitude", "wavelength", "frequency"], "correct": "square of amplitude", "cat": "Wave Optics", "diff": "Medium", "test_idx": 4},
        {"text": "The resolving power of a microscope is inversely proportional to", "type": "mcq", "options": ["wavelength", "aperture", "refractive index", "magnification"], "correct": "wavelength", "cat": "Wave Optics", "diff": "Hard", "test_idx": 4},
        {"text": "Unpolarized light can be converted into polarized light by", "type": "mcq", "options": ["reflection", "refraction", "scattering", "all of the above"], "correct": "all of the above", "cat": "Wave Optics", "diff": "Medium", "test_idx": 4},
        {"text": "Malus's law describes the intensity of light transmitted through a", "type": "mcq", "options": ["prism", "lens", "polarizer", "grating"], "correct": "polarizer", "cat": "Wave Optics", "diff": "Hard", "test_idx": 4},
        {"text": "The phenomenon of diffraction is more pronounced for", "type": "mcq", "options": ["short wavelengths", "long wavelengths", "high frequencies", "low frequencies"], "correct": "long wavelengths", "cat": "Wave Optics", "diff": "Medium", "test_idx": 4},

        # Unit 8 : Dual Nature of Radiation and Matter
        {"text": "The photoelectric effect demonstrates the", "type": "mcq", "options": ["wave nature of light", "particle nature of light", "both", "none"], "correct": "particle nature of light", "cat": "Dual Nature", "diff": "Easy", "test_idx": 4},
        {"text": "The work function of a metal is the minimum energy required to", "type": "mcq", "options": ["heat the metal", "emit an electron", "ionize the atom", "create a photon"], "correct": "emit an electron", "cat": "Dual Nature", "diff": "Easy", "test_idx": 4},
        {"text": "Einstein's photoelectric equation is", "type": "mcq", "options": ["E = hf", "K_max = hf - Φ", "λ = h/p", "E = mc²"], "correct": "K_max = hf - Φ", "cat": "Dual Nature", "diff": "Medium", "test_idx": 4},
        {"text": "The de Broglie wavelength of a particle is given by", "type": "mcq", "options": ["λ = h/p", "λ = hf", "λ = c/f", "λ = E/c"], "correct": "λ = h/p", "cat": "Dual Nature", "diff": "Easy", "test_idx": 4},
        {"text": "Matter waves are associated with", "type": "mcq", "options": ["photons", "electrons", "protons", "all moving particles"], "correct": "all moving particles", "cat": "Dual Nature", "diff": "Medium", "test_idx": 4},
        {"text": "The Davisson-Germer experiment confirmed the", "type": "mcq", "options": ["wave nature of electrons", "particle nature of electrons", "wave nature of light", "particle nature of light"], "correct": "wave nature of electrons", "cat": "Dual Nature", "diff": "Hard", "test_idx": 4},
        {"text": "The stopping potential in photoelectric effect depends on", "type": "mcq", "options": ["intensity of light", "frequency of light", "distance of source", "area of cathode"], "correct": "frequency of light", "cat": "Dual Nature", "diff": "Medium", "test_idx": 4},
        {"text": "Photons are quanta of", "type": "mcq", "options": ["matter", "energy", "charge", "momentum"], "correct": "energy", "cat": "Dual Nature", "diff": "Easy", "test_idx": 4},
        {"text": "The momentum of a photon is", "type": "mcq", "options": ["hf/c", "h/λ", "E/c", "all of the above"], "correct": "all of the above", "cat": "Dual Nature", "diff": "Hard", "test_idx": 4},
        {"text": "The intensity of incident radiation affects the", "type": "mcq", "options": ["kinetic energy of emitted electrons", "stopping potential", "number of emitted electrons", "work function"], "correct": "number of emitted electrons", "cat": "Dual Nature", "diff": "Medium", "test_idx": 4},
        {"text": "X-rays are produced when fast-moving electrons are suddenly stopped by a metal target.", "type": "mcq", "options": ["True", "False", "Sometimes", "Depends on target"], "correct": "True", "cat": "Dual Nature", "diff": "Easy", "test_idx": 4},
        {"text": "The minimum wavelength of X-rays produced is inversely proportional to the", "type": "mcq", "options": ["accelerating voltage", "current", "target material", "filament temperature"], "correct": "accelerating voltage", "cat": "Dual Nature", "diff": "Hard", "test_idx": 4},
        {"text": "Compton effect demonstrates the", "type": "mcq", "options": ["wave nature of light", "particle nature of light", "wave nature of matter", "particle nature of matter"], "correct": "particle nature of light", "cat": "Dual Nature", "diff": "Hard", "test_idx": 4},
        {"text": "The energy of a photon is directly proportional to its", "type": "mcq", "options": ["wavelength", "frequency", "speed", "amplitude"], "correct": "frequency", "cat": "Dual Nature", "diff": "Easy", "test_idx": 4},
        {"text": "Electron microscope works on the principle of", "type": "mcq", "options": ["wave nature of electrons", "particle nature of electrons", "ray optics", "wave optics"], "correct": "wave nature of electrons", "cat": "Dual Nature", "diff": "Medium", "test_idx": 4},

        # Physics Part 1 (Units 1-4)
        # Unit 1 : Electrostatics
        {"text": "Coulomb’s law is strictly valid only when the charges are", "type": "mcq", "options": ["uniformly distributed", "stationary and point charges", "moving charges", "macroscopic bodies"], "correct": "stationary and point charges", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "The SI unit of electric flux is", "type": "mcq", "options": ["N C⁻¹", "N m² C⁻¹", "C m⁻²", "N m C⁻¹"], "correct": "N m² C⁻¹", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "The electric field inside a charged conductor is zero because", "type": "mcq", "options": ["charges are destroyed", "charges reside on surface", "permittivity is zero", "electric force is infinite"], "correct": "charges reside on surface", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Gauss law is most useful when the charge distribution has", "type": "mcq", "options": ["random symmetry", "cylindrical, spherical or planar symmetry", "irregular shape", "moving charges"], "correct": "cylindrical, spherical or planar symmetry", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Electrostatic force between two charges decreases in water because", "type": "mcq", "options": ["water absorbs charge", "dielectric constant is high", "distance increases", "charge leaks"], "correct": "dielectric constant is high", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Unit vector in Coulomb’s law represents", "type": "mcq", "options": ["magnitude of force", "distance", "direction of force", "charge density"], "correct": "direction of force", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Dimensional formula of electric field is", "type": "mcq", "options": ["[MLT⁻³A⁻¹]", "[MLT⁻²A⁻¹]", "[ML²T⁻³A⁻¹]", "[ML⁻¹T⁻²A⁻¹]"], "correct": "[MLT⁻³A⁻¹]", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Electric potential is a", "type": "mcq", "options": ["scalar quantity", "vector quantity", "tensor quantity", "pseudo vector"], "correct": "scalar quantity", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Equipotential surfaces are always", "type": "mcq", "options": ["parallel to electric field", "perpendicular to electric field", "inclined to electric field", "circular to field"], "correct": "perpendicular to electric field", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Capacitance depends on", "type": "mcq", "options": ["charge", "potential difference", "geometry of conductor", "dielectric strength"], "correct": "geometry of conductor", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "SI unit of capacitance is", "type": "mcq", "options": ["Coulomb", "Volt", "Farad", "Tesla"], "correct": "Farad", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Energy stored in a capacitor depends on", "type": "mcq", "options": ["Q only", "V only", "both Q and V", "dielectric only"], "correct": "both Q and V", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Electric dipole moment is directed from", "type": "mcq", "options": ["–q to +q", "+q to –q", "centre outward", "perpendicular to axis"], "correct": "–q to +q", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Van de Graaff generator works on the principle of", "type": "mcq", "options": ["electromagnetic induction", "electrostatic induction", "corona discharge", "mutual induction"], "correct": "electrostatic induction", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        {"text": "Sharp points on conductors produce corona discharge due to", "type": "mcq", "options": ["low electric field", "high electric field", "uniform charge distribution", "zero potential"], "correct": "high electric field", "cat": "Electrostatics", "diff": "Easy", "test_idx": 3},
        
        # Unit 2 : Current Electricity
        {"text": "Drift velocity of electrons increases when", "type": "mcq", "options": ["temperature increases", "electric field increases", "resistance increases", "length increases"], "correct": "electric field increases", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "SI unit of resistivity is", "type": "mcq", "options": ["Ω", "Ω m", "Ω m⁻¹", "m Ω"], "correct": "Ω m", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Ohm’s law is valid only when", "type": "mcq", "options": ["temperature is constant", "voltage is high", "resistance is zero", "current is maximum"], "correct": "temperature is constant", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Wheatstone bridge is used to", "type": "mcq", "options": ["measure current", "measure voltage", "compare resistances", "store charge"], "correct": "compare resistances", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Kirchhoff’s junction rule is based on", "type": "mcq", "options": ["energy conservation", "charge conservation", "momentum conservation", "power conservation"], "correct": "charge conservation", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Temperature coefficient of resistance for metals is", "type": "mcq", "options": ["zero", "negative", "positive", "infinite"], "correct": "positive", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "EMF of a cell is independent of", "type": "mcq", "options": ["current", "external resistance", "internal resistance", "chemical reaction"], "correct": "external resistance", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Terminal voltage is less than EMF when the cell", "type": "mcq", "options": ["is idle", "supplies current", "is disconnected", "is fully charged"], "correct": "supplies current", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Power dissipated in a resistor is maximum when", "type": "mcq", "options": ["R = 0", "R = ∞", "R = internal resistance", "R is minimum"], "correct": "R = internal resistance", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Drift velocity is of the order of", "type": "mcq", "options": ["speed of light", "sound velocity", "mm/s", "km/s"], "correct": "mm/s", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Conductivity is reciprocal of", "type": "mcq", "options": ["resistance", "resistivity", "current", "voltage"], "correct": "resistivity", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Superconductors have resistivity", "type": "mcq", "options": ["zero", "infinite", "constant", "negative"], "correct": "zero", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Ammeter is connected in", "type": "mcq", "options": ["parallel", "series", "mixed", "diagonal"], "correct": "series", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Voltmeter resistance should be", "type": "mcq", "options": ["low", "zero", "infinite", "negative"], "correct": "infinite", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        {"text": "Kirchhoff’s loop rule follows from", "type": "mcq", "options": ["charge conservation", "energy conservation", "mass conservation", "momentum conservation"], "correct": "energy conservation", "cat": "Current Electricity", "diff": "Easy", "test_idx": 3},
        
        # Unit 3 : Magnetism
        {"text": "SI unit of magnetic field is", "type": "mcq", "options": ["Weber", "Tesla", "Henry", "Gauss"], "correct": "Tesla", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Fleming’s left hand rule is used to find", "type": "mcq", "options": ["direction of current", "direction of force", "direction of field", "magnitude of force"], "correct": "direction of force", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Magnetic field at centre of circular coil increases with", "type": "mcq", "options": ["radius", "current", "resistance", "temperature"], "correct": "current", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Lorentz force acts on", "type": "mcq", "options": ["stationary charge", "moving charge", "neutral particle", "photon"], "correct": "moving charge", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Force on a charge moving parallel to magnetic field is", "type": "mcq", "options": ["maximum", "zero", "minimum", "infinite"], "correct": "zero", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Right hand thumb rule is used to find", "type": "mcq", "options": ["direction of current", "direction of force", "direction of magnetic field", "magnitude of field"], "correct": "direction of magnetic field", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Magnetic field lines form", "type": "mcq", "options": ["open curves", "closed loops", "straight lines", "broken paths"], "correct": "closed loops", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "SI unit of magnetic flux is", "type": "mcq", "options": ["Tesla", "Weber", "Henry", "Ampere"], "correct": "Weber", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Torque on a magnetic dipole is maximum when", "type": "mcq", "options": ["θ = 0°", "θ = 90°", "θ = 180°", "θ = 45°"], "correct": "θ = 90°", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Magnetic moment of current loop depends on", "type": "mcq", "options": ["current only", "area only", "current and area", "resistance"], "correct": "current and area", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Moving coil galvanometer works on", "type": "mcq", "options": ["electromagnetic induction", "torque on current loop", "Lorentz force", "Hall effect"], "correct": "torque on current loop", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Earth’s magnetic field is due to", "type": "mcq", "options": ["permanent magnet", "electric currents in core", "iron deposits", "solar wind"], "correct": "electric currents in core", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Cyclotron cannot accelerate", "type": "mcq", "options": ["electrons", "protons", "alpha particles", "deuterons"], "correct": "electrons", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Magnetic permeability is maximum for", "type": "mcq", "options": ["diamagnetic", "paramagnetic", "ferromagnetic", "vacuum"], "correct": "ferromagnetic", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        {"text": "Magnetic susceptibility is negative for", "type": "mcq", "options": ["paramagnetic", "ferromagnetic", "diamagnetic", "superconductors"], "correct": "diamagnetic", "cat": "Magnetism", "diff": "Easy", "test_idx": 3},
        
        # Unit 4 : EMI & AC
        {"text": "Faraday’s law relates induced EMF with", "type": "mcq", "options": ["current", "resistance", "magnetic flux", "electric field"], "correct": "magnetic flux", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Lenz’s law obeys", "type": "mcq", "options": ["momentum conservation", "energy conservation", "charge conservation", "mass conservation"], "correct": "energy conservation", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Self induction occurs when", "type": "mcq", "options": ["current in nearby coil changes", "current in same coil changes", "resistance changes", "voltage is zero"], "correct": "current in same coil changes", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "SI unit of inductance is", "type": "mcq", "options": ["Tesla", "Henry", "Weber", "Ohm"], "correct": "Henry", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Eddy currents are produced due to", "type": "mcq", "options": ["changing magnetic flux", "constant current", "static field", "electric field"], "correct": "changing magnetic flux", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Transformer works on", "type": "mcq", "options": ["mutual induction", "self induction", "electromagnetic force", "Hall effect"], "correct": "mutual induction", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Step-up transformer increases", "type": "mcq", "options": ["current", "voltage", "power", "frequency"], "correct": "voltage", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "RMS value of AC current is", "type": "mcq", "options": ["peak value", "zero", "average value", "0.707 × peak value"], "correct": "0.707 × peak value", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Power factor is maximum when", "type": "mcq", "options": ["circuit is inductive", "circuit is capacitive", "circuit is resistive", "frequency is zero"], "correct": "circuit is resistive", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Choke coil is used to", "type": "mcq", "options": ["increase power loss", "reduce AC current", "store charge", "generate EMF"], "correct": "reduce AC current", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "AC frequency in India is", "type": "mcq", "options": ["60 Hz", "50 Hz", "25 Hz", "100 Hz"], "correct": "50 Hz", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Impedance is AC equivalent of", "type": "mcq", "options": ["current", "resistance", "voltage", "power"], "correct": "resistance", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Reactance of capacitor decreases when", "type": "mcq", "options": ["frequency decreases", "frequency increases", "voltage increases", "current increases"], "correct": "frequency increases", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "LC oscillations occur due to", "type": "mcq", "options": ["energy loss", "energy transfer between L and C", "resistance", "power dissipation"], "correct": "energy transfer between L and C", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
        {"text": "Q-factor of resonance is a measure of", "type": "mcq", "options": ["power loss", "sharpness of resonance", "current", "voltage"], "correct": "sharpness of resonance", "cat": "EMI & AC", "diff": "Easy", "test_idx": 3},
    ]

    print(f"Seeding {len(questions_list)} questions...")
    new_count = 0
    for q in questions_list:
        if q['test_idx'] >= len(test_ids):
            continue
            
        test_id = test_ids[q['test_idx']]
        if not Question.query.filter_by(test_id=test_id, text=q['text']).first():
            new_q = Question(
                test_id=test_id,
                text=q['text'],
                type=q['type'],
                options=json.dumps(q['options']),
                correct_answer=q['correct'],
                category=q['cat'],
                difficulty=q['diff']
            )
            db.session.add(new_q)
            new_count += 1

    print(f"Added {new_count} new questions.")

    db.session.commit()
    print("Database seeded successfully.")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_db()
