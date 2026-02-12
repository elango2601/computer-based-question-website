import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_django.settings')
django.setup()

from exams.models import Test

def seed():
    today = datetime.date.today()
    
    tests_data = [
        {"title": "Physics Phase 1", "desc": "Units 1-4", "date": today, "duration": 90},
        {"title": "Physics Phase 2", "desc": "Units 5-8", "date": today + datetime.timedelta(days=1), "duration": 90},
        {"title": "Physics Phase 3", "desc": "Units 9-11", "date": today + datetime.timedelta(days=2), "duration": 90},
        {"title": "Maths Revision 2 Phase 1", "desc": "Matrices, Complex Numbers, Theory of Equations, Inverse Trig", "date": today + datetime.timedelta(days=3), "duration": 90},
        {"title": "Maths Revision 2 Phase 2", "desc": "Units 5-8", "date": today + datetime.timedelta(days=4), "duration": 90},
        {"title": "Maths Revision 2 Phase 3", "desc": "Units 9-12", "date": today + datetime.timedelta(days=5), "duration": 90},
    ]
    
    for item in tests_data:
        t, created = Test.objects.get_or_create(
            title=item['title'],
            defaults={
                'description': item['desc'],
                'scheduled_date': item['date'],
                'duration_minutes': item['duration'],
                'has_compiler': False,
                'is_active': True
            }
        )
        if created:
            print(f"Created Test: {item['title']} (ID: {t.id})")
        else:
            print(f"Test Exists: {item['title']} (ID: {t.id})")

if __name__ == "__main__":
    seed()
