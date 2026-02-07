from app import app, db
from models import Test
from datetime import date

def fix_dates():
    with app.app_context():
        # Get all tests
        tests = Test.query.all()
        today = date.today()
        
        print(f"Updating test dates to {today}...")
        
        for t in tests:
            if "Phase 2" in t.title or "Phase 3" in t.title:
                t.scheduled_date = today
                print(f"Updated {t.title} to Today ({today})")
            elif "Phase 1" in t.title:
                # Keep phase 1 as is or update if needed. Assuming phase 1 is done.
                # But if user wants ALL, I can update all.
                # User specifically mentioned Phase 2 and 3.
                pass
                
        db.session.commit()
        print("Dates updated successfully.")

if __name__ == '__main__':
    fix_dates()
