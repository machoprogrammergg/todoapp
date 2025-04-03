from flask import flash, Blueprint, request, render_template, redirect, url_for
from .models import UserAccount
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user



auth = Blueprint('auth', __name__)


def userExists(givenEmail):
    search = db.session.query(UserAccount).filter_by(email=givenEmail).first()
    return search is not None
    
def isUsernameValid(givenName):
    search = db.session.query(UserAccount).filter_by(name=givenName).first()
    return search is not None

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        inputEmail = request.form.get('email')
        inputName = request.form.get('username')
        inputPassword = request.form.get('password')
        con_password = request.form.get('con_password')

        if len(inputEmail) < 4:
            flash('Email too short! Please enter a valid email address.', category='error')
        elif userExists(inputEmail):
            flash('An account with this email already exists!', category='error')
        elif isUsernameValid(inputName):
            flash('Username already taken!', category='error')
        elif len(inputPassword) < 7:
            flash('Password must have 7 or more letters!', category='error')
        elif inputPassword != con_password:
            flash('Passwords do not match!', category='error')
        else:
            new_user = UserAccount(email=inputEmail, password=generate_password_hash(inputPassword, 'scrypt'), name=inputName, task_count=0)
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created Successfully!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        inputEmail = request.form.get('email')
        inputPassword = request.form.get('password')
        user = db.session.query(UserAccount).filter_by(email=inputEmail).first()
        
        if userExists(inputEmail):
            if check_password_hash(user.password, inputPassword):
                login_user(user, remember=True)
                flash('Logged In Successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Password Incorrect. Please try again', category='error')
        else:
            flash(f'No account associated with email {inputEmail}', category='error')
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))