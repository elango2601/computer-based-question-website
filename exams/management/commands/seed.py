from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Test, Question
import datetime
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")
        
        # USERS
        users_data = [
            ('elangoadmin', 'elangoadmin123', 'admin'),
            ('student', 'student123', 'student'),
            ('Lathika16', 'Lathika16', 'student'),
            ('Sharuhasan', 'Sharuhasan29', 'student')
        ]
        
        for username, password, role in users_data:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password, role=role)
                self.stdout.write(f"User {username} created.")
        
        # TESTS
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)
        
        tests_data = [
            ("Maths Phase 1 (Units 1-4)", "Topics: Matrices, Complex Numbers, Theory of Eq, Inv. Trig", yesterday),
            ("Maths Phase 2 (Units 5-8)", "Topics: Two Dimensional Analytical Geometry – II, Applications of Vector Algebra, Applications of Differential Calculus, Differentials and Partial Derivatives", yesterday),
            ("Maths Phase 3 (Units 9-12)", "Topics: Applications of Integration,Ordinary Differential Equations,Probability Distributions,Discrete Mathematics", today),
            ("Physics Phase 1 (Units 1-4)", "Topics: Electrostatics, Current Electricity, Magnetism, EMI & AC", today),
            ("Physics Phase 2 (Units 5-8)", "Topics: EM Waves, Ray Optics, Wave Optics, Dual Nature", today),
            ("Physics Phase 3 (Units 9-12)", "Topics: Atomic Physics, Electronics, Recent Developments, Communication", today),
            ("Maths Revision 2 Phase 1 (Units 1-4)", "Topics: Matrices, Complex Numbers, Theory of Eq, Inv. Trig", tomorrow),
            ("Maths Revision 2 Phase 2 (Units 5-8)", "Topics: Analytical Geometry, Vector Algebra, Calculus", tomorrow),
            ("Maths Revision 2 Phase 3 (Units 9-12)", "Topics: Integration, ODE, Probability, Discrete Math", tomorrow)
        ]
        
        test_objects = []
        for title, desc, dt in tests_data:
            t, created = Test.objects.update_or_create(
                title=title,
                defaults={'description': desc, 'scheduled_date': dt}
            )
            test_objects.append(t)
            if created:
                self.stdout.write(f"Created Test: {title}")
            else:
                self.stdout.write(f"Updated Test: {title}")

        from exams.seed_data_list import questions_list

        count = 0
        for q in questions_list:
            # Use 'options' directly
            # The format in seed_data_list is a list of dicts.
            if q.get('test_idx') is None:
                continue
            
            # test_idx is 1-based in seed_data (1..6)
            # test_objects is 0-indexed list of created tests.
            # In seed_data, test_idx=1 corresponds to test_ids[0] (Maths Phase 1) IF test_ids order matches tests_data defined in seed_data.py.
            # In my Django seed.py, tests_data matches seed_data.py.
            # So test_idx=1 -> test_objects[0].
            # test_idx=2 (Unit 9-12) -> test_objects[2]. Wait.
            # seed_data.py: 
            # test_ids = []
            # tests_data = [...]
            # for ...: test_ids.append(t.id)
            # test_idx: 1 (Maths Phase 2) -> test_ids[1]? No.
            # seed_data: "Maths Phase 1", "Maths Phase 2", "Maths Phase 3"...
            # Line 95: test_idx: 1. "Maths Phase 2" is index 1.
            # So test_idx matches the index in tests_data list?
            # Yes. 1-based index? No, seed_data uses 1-based or 0-based?
            # Let's check seed_data line 95: test_idx: 1.
            # tests_data[1] is "Maths Phase 2".
            # questions "Unit 5 - 2D Analytical Geometry II". That matches Maths Phase 2.
            # So test_idx is 0-based index into tests_data? No. 1 is Phase 2. Phase 1 is index 0.
            # So test_idx 1 corresponds to index 1.
            
            idx = q['test_idx']
            if idx >= len(test_objects):
                self.stdout.write(f"Warning: test_idx {idx} out of range (max {len(test_objects)-1})")
                continue
                
            test = test_objects[idx]
            
            if not Question.objects.filter(test=test, text=q['text']).exists():
                Question.objects.create(
                    test=test,
                    text=q['text'],
                    type=q['type'],
                    options=q['options'], 
                    correct_answer=q['correct'],
                    category=q['cat'],
                    difficulty=q['diff']
                )
                count += 1
        
        self.stdout.write(f"Added {count} questions.")
