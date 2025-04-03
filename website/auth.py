from flask import flash, Blueprint, request, render_template, redirect, url_for  # Import necessary Flask functions
from .models import UserAccount  # Import UserAccount model to interact with the user data
from . import db  # Import db to interact with the database
from werkzeug.security import generate_password_hash, check_password_hash  # For securely hashing passwords and verifying them
from flask_login import login_user, logout_user, login_required, current_user  # Import Flask-Login functions for managing user sessions

# Create a blueprint for the 'auth' routes (authentication-related)
auth = Blueprint('auth', __name__)  

# Function to check if a user already exists based on the provided email
def userExists(givenEmail):
    search = db.session.query(UserAccount).filter_by(email=givenEmail).first()  # Search for an existing user by email
    return search is not None  # Return True if user exists, else False

# Function to check if the given username is already taken
def isUsernameValid(givenName):
    search = db.session.query(UserAccount).filter_by(name=givenName).first()  # Search for an existing user by username
    return search is not None  # Return True if username exists, else False

# Sign Up route: Handles both GET (render the sign-up page) and POST (form submission)
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # If form is submitted (POST request)
        # Retrieve form data
        inputEmail = request.form.get('email')
        inputName = request.form.get('username')
        inputPassword = request.form.get('password')
        con_password = request.form.get('con_password')

        # Validate input fields
        if len(inputEmail) < 4:
            flash('Email too short! Please enter a valid email address.', category='error')  # Show error if email is too short
        elif userExists(inputEmail):
            flash('An account with this email already exists!', category='error')  # Show error if email is already in use
        elif isUsernameValid(inputName):
            flash('Username already taken!', category='error')  # Show error if username is already in use
        elif len(inputPassword) < 7:
            flash('Password must have 7 or more letters!', category='error')  # Show error if password is too short
        elif inputPassword != con_password:
            flash('Passwords do not match!', category='error')  # Show error if passwords do not match
        else:
            # If all validations pass, create a new user and save to the database
            new_user = UserAccount(email=inputEmail, password=generate_password_hash(inputPassword, 'scrypt'), name=inputName, task_count=0)
            db.session.add(new_user)  # Add the new user to the session
            db.session.commit()  # Commit the changes to the database
            flash('Account Created Successfully!', category='success')  # Show success message
            login_user(new_user, remember=True)  # Log the user in after creation
            return redirect(url_for('views.home'))  # Redirect to the home page
    return render_template('signup.html', user=current_user)  # Render the sign-up page template for GET requests

# Login route: Handles both GET (render the login page) and POST (form submission)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If form is submitted (POST request)
        # Retrieve form data
        inputEmail = request.form.get('email')
        inputPassword = request.form.get('password')
        
        # Check if the user exists by email
        user = db.session.query(UserAccount).filter_by(email=inputEmail).first()
        
        if userExists(inputEmail):  # If user exists
            if check_password_hash(user.password, inputPassword):  # Check if password matches the stored hash
                login_user(user, remember=True)  # Log the user in
                flash('Logged In Successfully!', category='success')  # Show success message
                return redirect(url_for('views.home'))  # Redirect to the home page
            else:
                flash('Password Incorrect. Please try again', category='error')  # Show error if password is incorrect
        else:
            flash(f'No account associated with email {inputEmail}', category='error')  # Show error if no user is found with the given email
    return render_template('login.html', user=current_user)  # Render the login page template for GET requests

# Logout route: Logs out the current user
@auth.route('/logout')
@login_required  # Ensure that the user is logged in before accessing this route
def logout():
    logout_user()  # Log out the current user
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout
