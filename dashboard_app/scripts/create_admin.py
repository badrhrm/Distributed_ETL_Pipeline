# src/initial_data.py

import os
from dotenv import load_dotenv
from src.extensions import db
from src.models.user import User

def create_admin_if_not_exists(app):
    load_dotenv()

    with app.app_context():
        username = os.getenv('ADMIN_USERNAME')
        password = os.getenv('ADMIN_PASSWORD')

        if User.query.filter_by(username=username).first():
            print("✅ Admin user already exists.")
        else:
            admin = User(username=username)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created.")
