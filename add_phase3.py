from app import app, db
from models import Test, Question
import json
from datetime import date, timedelta

def add_questions():
    with app.app_context():
        # Find Phase 3 Test
        test = Test.query.filter(Test.title.like('%Phase 3%')).first()
        if not test:
            print("Phase 3 Test not found! Creating it...")
            t = Test(title="Maths Phase 3 (Units 9-12)", 
                     description="Topics: Integration, Diff. Equations, Probability, Discrete Math", 
                     scheduled_date=date.today())
            db.session.add(t)
            db.session.commit()
            test = t
        else:
            print(f"Found Test: {test.title}")
            
        # CLEAR EXISTING QUESTIONS FOR PHASE 3 (To ensure exactly 60)
        print(f"Clearing existing questions for {test.title}...")
        Question.query.filter_by(test_id=test.id).delete()
        db.session.commit()

        # Full 60 Question List
        questions_data = [
            # Q1-Q10 Easy
            {"text": "The integral of x is", "type": "mcq", "options": ["x", "x²", "x²/2", "ln x"], "correct": "x²/2", "cat": "Integration", "diff": "Easy"},
            {"text": "The order of the differential equation dy/dx = x is", "type": "mcq", "options": ["0", "1", "2", "3"], "correct": "1", "cat": "Diff Equations", "diff": "Easy"},
            {"text": "The probability of a sure event is", "type": "mcq", "options": ["0", "-1", "1", "∞"], "correct": "1", "cat": "Probability", "diff": "Easy"},
            {"text": "A statement which is either true or false is called", "type": "mcq", "options": ["sentence", "proposition", "equation", "variable"], "correct": "proposition", "cat": "Discrete Math", "diff": "Easy"},
            {"text": "The symbol used for integration is", "type": "mcq", "options": ["∂", "Δ", "∫", "Σ"], "correct": "∫", "cat": "Integration", "diff": "Easy"},
            {"text": "The degree of (dy/dx)² = x is", "type": "mcq", "options": ["1", "2", "0", "not defined"], "correct": "2", "cat": "Diff Equations", "diff": "Easy"},
            {"text": "The mean of a probability distribution is also called", "type": "mcq", "options": ["variance", "expectation", "standard deviation", "mode"], "correct": "expectation", "cat": "Probability", "diff": "Easy"},
            {"text": "The negation of the statement p is", "type": "mcq", "options": ["p", "¬p", "p ∧ q", "p ∨ q"], "correct": "¬p", "cat": "Discrete Math", "diff": "Easy"},
            {"text": "The area under a curve is found by", "type": "mcq", "options": ["differentiation", "integration", "limits", "matrices"], "correct": "integration", "cat": "Integration", "diff": "Easy"},
            {"text": "A random variable takes", "type": "mcq", "options": ["letters", "symbols", "numerical values", "words"], "correct": "numerical values", "cat": "Probability", "diff": "Easy"},

            # Q11-Q30 Medium (Part B)
            {"text": "∫(0 to 1) x² dx =", "type": "mcq", "options": ["1", "1/2", "1/3", "2"], "correct": "1/3", "cat": "Integration", "diff": "Medium"},
            {"text": "Area bounded by y=x, x-axis and x=2 is", "type": "mcq", "options": ["1", "2", "4", "3"], "correct": "2", "cat": "Integration", "diff": "Medium"},
            {"text": "The volume obtained by revolving about x-axis is found using", "type": "mcq", "options": ["shell method", "disk method", "trapezium rule", "Simpson’s rule"], "correct": "disk method", "cat": "Integration", "diff": "Medium"},
            {"text": "∫ e^x dx equals", "type": "mcq", "options": ["xe^x", "e^x + C", "e^x + 1", "ln x"], "correct": "e^x + C", "cat": "Integration", "diff": "Medium"},
            {"text": "∫ cos x dx =", "type": "mcq", "options": ["sin x + C", "-sin x + C", "tan x + C", "-cos x + C"], "correct": "sin x + C", "cat": "Integration", "diff": "Medium"},
            {"text": "The order of d²y/dx² + dy/dx = 0 is", "type": "mcq", "options": ["1", "2", "3", "0"], "correct": "2", "cat": "Diff Equations", "diff": "Medium"},
            {"text": "The degree of (d²y/dx²)³ = x is", "type": "mcq", "options": ["1", "2", "3", "0"], "correct": "3", "cat": "Diff Equations", "diff": "Medium"},
            {"text": "The general solution of dy/dx = 0 is", "type": "mcq", "options": ["y = 0", "y = x", "y = c", "y = eˣ"], "correct": "y = c", "cat": "Diff Equations", "diff": "Medium"},
            {"text": "A differential equation containing only y and dy/dx is", "type": "mcq", "options": ["linear", "separable", "exact", "non-linear"], "correct": "separable", "cat": "Diff Equations", "diff": "Medium"},
            {"text": "The solution of dy/dx = y is", "type": "mcq", "options": ["y = x + C", "y = Ce^x", "y = Cx", "y = ln x"], "correct": "y = Ce^x", "cat": "Diff Equations", "diff": "Medium"},

            {"text": "If A and B are mutually exclusive, then", "type": "mcq", "options": ["P(A∩B)=1", "P(A∪B)=0", "P(A∩B)=0", "P(A)=P(B)"], "correct": "P(A∩B)=0", "cat": "Probability", "diff": "Medium"},
            {"text": "Mean of binomial distribution is", "type": "mcq", "options": ["nq", "np", "pq", "n"], "correct": "np", "cat": "Probability", "diff": "Medium"},
            {"text": "Variance of binomial distribution is", "type": "mcq", "options": ["np", "npq", "nq", "pq"], "correct": "npq", "cat": "Probability", "diff": "Medium"},
            {"text": "If P(A)=0.4, then P(A′)=", "type": "mcq", "options": ["0.6", "0.4", "1.4", "0"], "correct": "0.6", "cat": "Probability", "diff": "Medium"},
            {"text": "A fair coin is tossed. Probability of getting a head is", "type": "mcq", "options": ["0", "1", "1/2", "2"], "correct": "1/2", "cat": "Probability", "diff": "Medium"},
            
            {"text": "The truth value of p ∨ q is false when", "type": "mcq", "options": ["p is true", "q is true", "both are false", "both are true"], "correct": "both are false", "cat": "Discrete Math", "diff": "Medium"},
            {"text": "The negation of p ∧ q is", "type": "mcq", "options": ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∨ q", "p ∧ q"], "correct": "¬p ∨ ¬q", "cat": "Discrete Math", "diff": "Medium"},
            {"text": "Converse of 'If p then q' is", "type": "mcq", "options": ["If q then p", "If ¬p then ¬q", "p ∧ q", "p ∨ q"], "correct": "If q then p", "cat": "Discrete Math", "diff": "Medium"},
            {"text": "A binary operation on a set maps", "type": "mcq", "options": ["S → S", "S × S → S", "S → S × S", "S × S → R"], "correct": "S × S → S", "cat": "Discrete Math", "diff": "Medium"},
            {"text": "The statement p → q is false when", "type": "mcq", "options": ["p true, q true", "p false, q true", "p false, q false", "p true, q false"], "correct": "p true, q false", "cat": "Discrete Math", "diff": "Medium"},

            # Q31-Q40 Hard (Part C)
            {"text": "Area between curves y=x and y=x² in [0,1] is", "type": "mcq", "options": ["1/2", "1/3", "1/6", "2/3"], "correct": "1/6", "cat": "Integration", "diff": "Hard"},
            {"text": "The solution of dy/dx + y = 0 is", "type": "mcq", "options": ["y = Ce^x", "y = Ce^-x", "y = Cx", "y = 0"], "correct": "y = Ce^-x", "cat": "Diff Equations", "diff": "Hard"},
            {"text": "If X is a random variable with values 1,2,3 each having probability 1/3, then mean is", "type": "mcq", "options": ["1", "2", "3", "4"], "correct": "2", "cat": "Probability", "diff": "Hard"},
            {"text": "The negation of (p → q) is", "type": "mcq", "options": ["p → ¬q", "¬p → q", "p ∧ ¬q", "¬p ∧ q"], "correct": "p ∧ ¬q", "cat": "Discrete Math", "diff": "Hard"},
            {"text": "If P(A)=1, then A is a", "type": "mcq", "options": ["impossible event", "random event", "sure event", "equally likely event"], "correct": "sure event", "cat": "Probability", "diff": "Hard"},
            {"text": "Degree of dy/dx + y = 0 is", "type": "mcq", "options": ["1", "2", "0", "not defined"], "correct": "not defined", "cat": "Diff Equations", "diff": "Hard"}, # User Key says D (Note: mathematically 1)
            {"text": "The expectation of a constant k is", "type": "mcq", "options": ["0", "1", "k", "k²"], "correct": "k", "cat": "Probability", "diff": "Hard"},
            {"text": "The contrapositive of p → q is", "type": "mcq", "options": ["¬q → ¬p", "q → p", "¬p → ¬q", "p → ¬q"], "correct": "¬q → ¬p", "cat": "Discrete Math", "diff": "Hard"},
            {"text": "If two events are independent, then", "type": "mcq", "options": ["P(A∩B)=0", "P(A∩B)=P(A)+P(B)", "P(A∩B)=P(A)P(B)", "P(A)=P(B)"], "correct": "P(A∩B)=P(A)P(B)", "cat": "Probability", "diff": "Hard"},
            {"text": "The volume generated by revolving y=f(x) about y-axis uses", "type": "mcq", "options": ["disk method", "shell method", "Simpson rule", "trapezium rule"], "correct": "shell method", "cat": "Integration", "diff": "Hard"},

            # Q41-Q50 Medium
            {"text": "The area bounded by the curve y=x², x-axis and x = 2 is", "type": "mcq", "options": ["8/3", "4/3", "4", "2"], "correct": "8/3", "cat": "Integration", "diff": "Medium"},
            {"text": "The integral ∫(0 to 2) 3x² dx is", "type": "mcq", "options": ["4", "6", "8", "12"], "correct": "12", "cat": "Integration", "diff": "Medium"}, # User Key D (12)
            {"text": "The differential equation dy/dx = x² is", "type": "mcq", "options": ["linear", "separable", "homogeneous", "exact"], "correct": "separable", "cat": "Diff Equations", "diff": "Medium"},
            {"text": "The solution of dy/dx = 2x is", "type": "mcq", "options": ["y=x² + C", "y=2x + C", "y=x + C", "y=2x² + C"], "correct": "y=x² + C", "cat": "Diff Equations", "diff": "Medium"},
            {"text": "If P(A)=0.7, then the probability of not A is", "type": "mcq", "options": ["0.7", "0.3", "1.7", "0"], "correct": "0.3", "cat": "Probability", "diff": "Medium"},
            {"text": "The sum of probabilities of all possible outcomes of a random experiment is", "type": "mcq", "options": ["0", "less than 1", "greater than 1", "1"], "correct": "1", "cat": "Probability", "diff": "Medium"},
            {"text": "The truth value of the statement p ∧ q is true when", "type": "mcq", "options": ["p is true", "q is true", "both p and q are true", "both p and q are false"], "correct": "both p and q are true", "cat": "Discrete Math", "diff": "Medium"},
            {"text": "If p is false and q is true, then p → q is", "type": "mcq", "options": ["true", "false", "undefined", "depends on p"], "correct": "true", "cat": "Discrete Math", "diff": "Medium"},
            {"text": "Mean of probability distribution x:1,2,3 P(x):1/3,1/3,1/3 is", "type": "mcq", "options": ["1", "2", "3", "4"], "correct": "2", "cat": "Probability", "diff": "Medium"},
            {"text": "The solution of dy/dx + 2y = 0 is", "type": "mcq", "options": ["y = Ce^2x", "y = Ce^-2x", "y = 2Ce^x", "y = Cx^-2"], "correct": "y = Ce^-2x", "cat": "Diff Equations", "diff": "Medium"},

            # Q51-Q60 Hard
            {"text": "The area enclosed between the curves y=x and y=x³ in [0,1] is", "type": "mcq", "options": ["1/2", "1/4", "1/6", "1/12"], "correct": "1/12", "cat": "Integration", "diff": "Hard"}, # User Key D (1/12)
            {"text": "Volume by revolving y=x from x=0 to 1 about y-axis is", "type": "mcq", "options": ["1/2", "1/3", "1/4", "1/6"], "correct": "1/3", "cat": "Integration", "diff": "Hard"}, # User Key B
            {"text": "Order of (d³y/dx³)² + y = 0 is", "type": "mcq", "options": ["1", "2", "3", "6"], "correct": "3", "cat": "Diff Equations", "diff": "Hard"},
            {"text": "Degree of (dy/dx)³ + y = 0 is", "type": "mcq", "options": ["1", "2", "3", "not defined"], "correct": "3", "cat": "Diff Equations", "diff": "Hard"},
            {"text": "If X is a random variable with mean 5, then E(X − 2) is", "type": "mcq", "options": ["2", "3", "5", "7"], "correct": "3", "cat": "Probability", "diff": "Hard"},
            {"text": "If two events A and B are independent, then P(A∣B) =", "type": "mcq", "options": ["P(A+B)", "P(A)", "P(B)", "0"], "correct": "P(A)", "cat": "Probability", "diff": "Hard"}, # Note: options from question were slightly different, simplified here to match logic
            {"text": "Negation of 'p or q' is", "type": "mcq", "options": ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∧ q", "p → q"], "correct": "¬p ∧ ¬q", "cat": "Discrete Math", "diff": "Hard"},
            {"text": "Contrapositive of 'If p then q' is", "type": "mcq", "options": ["If q then p", "If ¬p then ¬q", "If ¬q then ¬p", "If p then ¬q"], "correct": "If ¬q then ¬p", "cat": "Discrete Math", "diff": "Hard"},
            {"text": "If P(A)=0.4, P(B)=0.5 and independent, then P(A ∩ B) is", "type": "mcq", "options": ["0.9", "0.2", "0.45", "0.1"], "correct": "0.2", "cat": "Probability", "diff": "Hard"},
            {"text": "p ↔ q is true when", "type": "mcq", "options": ["p is true and q is false", "p is false and q is true", "p and q have same truth value", "p and q have different truth values"], "correct": "p and q have same truth value", "cat": "Discrete Math", "diff": "Hard"},
        ]

        # Add to DB
        count = 0
        for q in questions_data:
            # Check for dupes by text AND test_id
            if not Question.query.filter_by(test_id=test.id, text=q['text']).first():
                new_q = Question(
                    test_id=test.id,
                    text=q['text'],
                    type=q['type'],
                    options=json.dumps(q['options']),
                    correct_answer=q['correct'],
                    category=q['cat'],
                    difficulty=q['diff']
                )
                db.session.add(new_q)
                count += 1
        
        db.session.commit()
        print(f"Added {count} questions to Phase 3.")

if __name__ == '__main__':
    add_questions()
