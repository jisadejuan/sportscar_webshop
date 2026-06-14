from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

# --- USER SIGN UP ---
@auth_bp.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Account already exists, please log in.', 'danger')
            return redirect(url_for('auth.user_login'))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account signed up successfully!', 'success')
        return redirect(url_for('auth.user_login'))

    return render_template('public/user_signup.html')

# --- USER LOGIN ---
@auth_bp.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id   # 👉 save user session
            flash('Login successful!', 'success')
            return redirect(url_for('product.home'))  # or user dashboard
        else:
            flash('No account found, please sign up first.', 'warning')
            return redirect(url_for('auth.user_signup'))

    # GET request → unified login page
    return render_template('login.html')
