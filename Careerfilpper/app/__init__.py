from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)

    # Register routes and create tables within the app context
    with app.app_context():
        from .routes import init_routes
        init_routes(app)

        # Create database tables if they don’t exist
        db.create_all()

    return app
