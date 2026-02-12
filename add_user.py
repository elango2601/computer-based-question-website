from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def add_user():
    with app.app_context():
        if not User.query.filter_by(username='Sharuhasan').first():
            hash_pw = generate_password_hash('Sharuhasan29')
            user = User(username='Sharuhasan', password=hash_pw, role='student')
            db.session.add(user)
            db.session.commit()
            print("Successfully added user: Sharuhasan")
        else:
            print("User Sharuhasan already exists.")

def add_user1():
    with app.app_context():
        if not User.query.filter_by(username='Aakash').first():
            hash_pw = generate_password_hash('Aakash29')
            user = User(username='Aakash', password=hash_pw, role='student')
            db.session.add(user)
            db.session.commit()
            print("Successfully added user: Aakash")
        else:
            print("User Aakash already exists.")

if __name__ == "__main__":
    add_user()
    add_user1()
