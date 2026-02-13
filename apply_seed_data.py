import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_django.settings')
django.setup()

from exams.models import Test, Question
from exams.seed_data_list import questions_list

# Mapping test_idx in seed_data to Test Titles in DB
TEST_MAP = {
    1: "Maths Revision 2 Phase 2",
    2: "Maths Revision 2 Phase 3",
    3: "Physics Phase 1",
    4: "Physics Phase 2",
    5: "Physics Phase 3",
    6: "Maths Revision 2 Phase 1"
}

def apply_seed():
    print("Applying seed data...")
    count = 0
    
    # Cache tests to avoid DB hits
    tests_cache = {}
    for idx, title in TEST_MAP.items():
        try:
            t = Test.objects.get(title=title)
            tests_cache[idx] = t
            # Optional: Clear existing questions to avoid duplicates?
            # t.questions.all().delete() 
            # Better: use get_or_create for questions
        except Test.DoesNotExist:
            print(f"Warning: Test '{title}' not found. Run seed_full.py first.")
            
    for q in questions_list:
        t_idx = q.get('test_idx')
        if t_idx not in tests_cache:
            continue
            
        test = tests_cache[t_idx]
        
        # Check if question exists
        if not Question.objects.filter(test=test, text=q['text']).exists():
            Question.objects.create(
                test=test,
                text=q['text'],
                options=q['options'],
                correct_answer=q['correct'],
                category=q['cat'],
                difficulty=q.get('diff', 'Medium'),
                type=q['type']
            )
            count += 1
            
    print(f"Successfully added {count} questions from seed_data_list.")

if __name__ == "__main__":
    apply_seed()
