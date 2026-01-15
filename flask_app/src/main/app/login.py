from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth_login = Blueprint('login', __name__)

@auth_login.route('/login')
def login():
    return render_template('login.html')

@auth_login.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login.login'))

    login_user(user)
    return redirect(url_for('main.profile'))

@auth_login.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')

        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            flash("Password successfully updated. You can now login.")
            return redirect(url_for('login.login'))
        else:
            flash("Email not found. Please check and try again.")
            return redirect(url_for('login.forgot_password'))

    return render_template('forgot_password.html')

@auth_login.route('/register')
def register():
    return render_template('register.html')

@auth_login.route('/register', methods=['POST'])
def register_post():

    email = request.form.get('email')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    # if true the email exists in the database, an unique email is required for registration, redirect to register page to try again
    user = User.query.filter_by(email=email).first() 
    if user: 
        flash('This email address already exists! Please try again!')
        return redirect(url_for('login.register'))

    # create and add new user to the database
    # new_user = User(email=email, name=name, last_name=last_name, password=password, role_id=1)
    new_user = User(email=email, name=name, last_name=last_name, role_id=1, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login.login'))

@auth_login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
