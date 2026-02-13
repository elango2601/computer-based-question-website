import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_django.settings')
django.setup()

from users.models import User

def create_admin():
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, 'admin@example.com', password, role='admin')
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")

    # Seed Students
    students = [
        ("sharuhasan", "sharuhasan29"),
        ("Lathika", "Lathika26"),
    ]
    for user, pwd in students:
        if not User.objects.filter(username=user).exists():
            User.objects.create_user(username=user, password=pwd, role='student')
            print(f"Created student: {user}")
        else:
            print(f"Student exists: {user}")

if __name__ == '__main__':
    create_admin()
