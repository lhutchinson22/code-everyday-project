from flask import Blueprint, request, redirect, url_for, render_template, flash
from .models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('views.signup'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return redirect(url_for('views.home'))
        else:
            flash('Login unsuccessful. Please check your username and password.')

    return render_template('login.html')
