from flask import session

def login_user(user):
    session['user_id'] = user.id
    session['username'] = user.username

def logout_user():
    session.clear()

def get_current_user():
    return session.get('username')
