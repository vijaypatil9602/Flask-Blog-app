from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Redirects to this page if user is not logged in
login_manager.login_message_category = 'info' # Bootstrap class for flash message

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from project.main.routes import main
    from project.auth.routes import auth
    from project.crud.routes import crud
    from project.dashboard.routes import dashboard
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(crud)
    app.register_blueprint(dashboard)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app