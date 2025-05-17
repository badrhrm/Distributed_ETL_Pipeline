from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.user import User
from src.controllers.auth import login_user, logout_user, get_current_user
from src.controllers.orchestration_controller import trigger_etl_process
from src.controllers.schedule_controller import update_schedule

main = Blueprint('main', __name__)

@main.route('/')
def home():
    username = get_current_user()
    if username:
        return render_template('home.html', username=username)
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.authenticate(username, password)
        if user:
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/trigger_etl', methods=['POST'])
def trigger_etl():
    message = trigger_etl_process()
    return render_template('home.html', message=message)

@main.route('/schedule', methods=['GET', 'POST'])
def update_schedule_view():
    if request.method == 'POST':
        return update_schedule()
    return render_template('set_schedule.html')