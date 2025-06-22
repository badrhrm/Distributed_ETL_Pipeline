# Importation des fonctions pour hacher et vérifier les mots de passe
from werkzeug.security import generate_password_hash, check_password_hash

# Importation de l'instance SQLAlchemy définie ailleurs dans l'application
from src.extensions import db  

# Définition du modèle User (utilisateur) lié à une table dans la base de données
class User(db.Model):
    # Identifiant unique de l'utilisateur (clé primaire auto-incrémentée)
    id = db.Column(db.Integer, primary_key=True)
    
    # Nom d'utilisateur, chaîne de caractères unique et non nulle
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Mot de passe haché, stocké de manière sécurisée (jamais en clair)
    password_hash = db.Column(db.String(128), nullable=False)

    # Méthode pour définir le mot de passe : il est transformé en hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Méthode pour vérifier si un mot de passe fourni correspond au hash enregistré
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Méthode statique d'authentification d'un utilisateur par nom d'utilisateur et mot de passe
    @staticmethod
    def authenticate(username, password):
        # Recherche de l'utilisateur dans la base par son nom
        user = User.query.filter_by(username=username).first()
        # Si l'utilisateur existe et que le mot de passe est correct, on le retourne
        if user and user.check_password(password):
            return user
        # Sinon, on retourne None pour indiquer un échec d'authentification
        return None
