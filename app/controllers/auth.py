from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.user import User

# Define the blueprint FIRST
auth_bp = Blueprint('auth', __name__)

# --- USER SIGN UP ---
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered, please log in.', 'danger')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Sign‑up successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('public/signup.html')

# --- USER LOGIN ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('product.home'))  # or redirect to user dashboard
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('public/login.html')
