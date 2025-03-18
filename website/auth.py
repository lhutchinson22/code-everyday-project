from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_login import login_user

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the email already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Redirect to the login page after signup
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            flash('Login successful!')
            return redirect(url_for('views.home'))
        else:
            flash('Login unsuccessful. Please check your username and password.')

    return render_template('login.html')
