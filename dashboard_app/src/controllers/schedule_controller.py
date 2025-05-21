from flask import request, redirect, url_for, flash
from src.controllers.orchestration_controller import update_orchestration_schedule

def update_schedule():
    if request.method == 'POST':
        day_of_week = request.form['day_of_week']
        hour = int(request.form['hour'])
        minute = int(request.form['minute'])

        try:
            update_orchestration_schedule(day_of_week, hour, minute)
            flash(f"ETL schedule updated to: {day_of_week} at {hour}:{minute}", 'success')
        except Exception as e:
            flash(f"Error updating schedule: {str(e)}", 'error')

        return redirect(url_for('main.home'))
