from flask import Flask
from config import Config
from src.extensions import db
from src.views.routes import main
from scripts.create_admin import create_admin_if_not_exists

def create_app():
    app = Flask(__name__, template_folder='src/templates' ,static_folder='src/static')
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    return app

def init_db(app):
    """ Initialize the database """
    with app.app_context():
        db.create_all()

def create_admin(app):
    """ Create the admin user if it does not exist """
    with app.app_context():
        create_admin_if_not_exists(app)

def run_app():
    """ Run the Flask app """
    app = create_app()
    init_db(app)
    create_admin(app)
    app.run(host='0.0.0.0', debug=True)

if __name__ == '__main__':
    run_app()