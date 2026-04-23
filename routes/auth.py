from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required
from db import db
from models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth_blueprint = Blueprint('auth', __name__)


# Sign Up Route
@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':
        return redirect(url_for('index'))

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        flash("All fields are required!", "danger")
        return redirect(url_for('index'))

    if User.query.filter_by(email=email).first():
        flash("Email already registered!", "danger")
        return redirect(url_for('index'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful! Please log in.", "success")
    return redirect(url_for('index'))


# Log In Route
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash("Email and password are required!", "danger")
        return redirect(url_for('index'))

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        flash("Invalid email or password!", "danger")
        return redirect(url_for('index'))

    login_user(user)
    flash(f"Welcome back, {user.name}!", "success")

    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('index'))

# Log Out Route
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()  # Logs out the current user
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))
