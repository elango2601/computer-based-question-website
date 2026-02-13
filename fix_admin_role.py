import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_django.settings')
django.setup()

from users.models import User

def fix_roles():
    count = User.objects.filter(is_superuser=True).update(role='admin')
    print(f"Updated {count} superusers to have role='admin'.")

if __name__ == "__main__":
    fix_roles()
