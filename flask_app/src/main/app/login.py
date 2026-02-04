from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Role
from . import db

auth_login = Blueprint('login', __name__)

@auth_login.route('/login')
def login():
    return render_template('login.html')

@auth_login.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Email and password are required.')
        return redirect(url_for('login.login'))

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login.login'))

    login_user(user, remember=False)
    return redirect(url_for('main.profile'))

@auth_login.route('/forgot_password', methods=['GET'])
def forgot_password_form():
    return render_template('forgot_password.html')

@auth_login.route('/forgot_password', methods=['POST'])
def forgot_password_submit():
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    
    if not email or not new_password:
        flash("Email and new password are required.")
        return redirect(url_for('login.forgot_password_form'))
    
    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        flash("Password successfully updated. You can now login.")
        return redirect(url_for('login.login'))
    else:
        flash("Email not found. Please check and try again.")
        return redirect(url_for('login.forgot_password_form'))

@auth_login.route('/register')
def register():
    return render_template('register.html')

@auth_login.route('/register', methods=['POST'])
def register_post():

    email = request.form.get('email')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    if not email or not name or not last_name or not password:
        flash('All fields are required!')
        return redirect(url_for('login.register'))

    user = User.query.filter_by(email=email).first() 
    if user: 
        flash('This email address already exists! Please try again!')
        return redirect(url_for('login.register'))

    customer_role = Role.query.filter_by(name='customer').first()
    new_user = User(email=email, name=name, last_name=last_name, role=customer_role, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login.login'))

@auth_login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
