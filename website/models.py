from flask_login import UserMixin  # Import UserMixin to handle user session management
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean  # Import necessary SQLAlchemy classes for defining columns and relationships
from . import db  # Import the db instance from the application to interact with the database


# UserAccount model: Represents the user in the application
class UserAccount(db.Model, UserMixin):
    __tablename__ = 'user_account'  # Name of the table in the database

    # Define columns in the 'user_account' table
    id = Column(Integer, primary_key=True)  # Unique identifier for each user
    name = Column(String)  # User's name
    email = Column(String, unique=True)  # User's email address (unique to prevent duplicate emails)
    password = Column(String)  # User's hashed password
    tasks = db.relationship('TaskList')  # One-to-many relationship: a user can have many tasks
    task_count = Column(Integer)  # Column to store the number of tasks the user has

    # Override the get_id method (required by Flask-Login for user session management)
    def get_id(self):
        return str(self.id)  # Returns the user's ID as a string for Flask-Login

    # is_authenticated method (checks if the user is authenticated in the session)
    def is_authenticated(self):
        return self.is_authenticated  # Return user's authentication status

    # is_active method (checks if the user account is active)
    def is_active(self):
        return self.is_active  # Return user's active status

    # is_anonymous method (always returns False for authenticated users)
    def is_anonymous(self):
        return False  # Since the user is authenticated, they are not anonymous

    # Optional: Represent the UserAccount instance as a string (for debugging purposes)
    def __repr__(self):
        return f"<UserAccount {self.name}>"  # Return a string that represents the user by name


# TaskList model: Represents a task assigned to a user
class TaskList(db.Model):
    __tablename__ = 'tasks'  # Name of the table in the database

    # Define columns in the 'tasks' table
    id = Column(Integer, primary_key=True)  # Unique identifier for each task
    title = Column(String)  # The title or name of the task
    note = Column(String)  # A note or description related to the task
    user_id = Column(Integer, ForeignKey('user_account.id'))  # Foreign key to link the task to a user account
    time_stamp = Column(String)  # Timestamp to store when the task was created or last updated
    completed = Column(Boolean)  # Boolean value to indicate if the task has been completed

