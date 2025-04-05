# Import necessary modules
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
import secrets

app = Flask(__name__)

# Initialize SQLAlchemy and set the database file name
db = SQLAlchemy()
DB_NAME = 'database.db'

# Function to create and configure the Flask application
def create_app():
    app.config['SECRET_KEY'] =  secrets.token_hex(16)  # Set a secret key for session management
    app.config['SQLALCHEMY_DATABASE_URI'] = F'sqlite:///{DB_NAME}'  # Set the URI for the SQLite database

    # Import views, authentication, and models modules (views and auth are blueprints for different app sections)
    from .views import views
    from .auth import auth
    from .models import UserAccount, TaskList  # Models for database entities

    # Initialize the database with the app
    db.init_app(app)

    # Ensure the database is created if it doesn't already exist
    create_database(app)

    # Initialize the LoginManager for user authentication
    login_manager = LoginManager()
    login_manager.login_view= 'auth.login'  # Set the login route for user redirection if not logged in
    login_manager.init_app(app)  # Initialize LoginManager with the app

    # User loader function to retrieve user by ID
    @login_manager.user_loader
    def load_user(id):
        return UserAccount.query.get(int(id))  # Query the database to load the user by their ID

    # Register blueprints for different sections of the app (views and authentication)
    app.register_blueprint(views, url_prefix='/')  # Register the views blueprint at the root URL
    app.register_blueprint(auth, url_prefix='/')  # Register the auth blueprint at the root URL

    return app  # Return the configured app

# Function to create the database if it does not exist
def create_database(e):
    # Check if the database file already exists
    if not path.exists(DB_NAME):  
        with e.app_context():  # Ensure the app context is available
            db.create_all()  # Create all the database tables based on the defined models
