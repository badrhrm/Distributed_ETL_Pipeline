from flask import request, redirect, url_for, flash
from src.controllers.orchestration_controller import update_orchestration_schedule

# Cette fonction gère la mise à jour de la planification de l’ETL via un formulaire HTML.
def update_schedule():
    # Vérifie si la méthode HTTP est POST (ce qui signifie que le formulaire a été soumis)
    if request.method == 'POST':
        # Récupère les valeurs du jour, de l'heure et des minutes depuis le formulaire
        day_of_week = request.form['day_of_week']   # ex: 'Monday'
        hour = int(request.form['hour'])            # ex: 14
        minute = int(request.form['minute'])        # ex: 30

        try:
            # Appelle la fonction qui met à jour la planification de l’orchestration ETL
            update_orchestration_schedule(day_of_week, hour, minute)
            # Affiche un message de succès à l’utilisateur
            flash(f"ETL schedule updated to: {day_of_week} at {hour}:{minute}", 'success')
        except Exception as e:
            # Si une erreur survient, affiche un message d'erreur à l'utilisateur
            flash(f"Error updating schedule: {str(e)}", 'error')

        # Redirige l’utilisateur vers la page d’accueil de l’application
        return redirect(url_for('main.home'))

