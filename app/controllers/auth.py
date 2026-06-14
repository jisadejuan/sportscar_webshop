from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Account already exists, please log in.', 'danger')
            return redirect(url_for('auth.login'))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account signed up successfully!', 'success')
        return redirect(url_for('auth.login'))

    # ✅ Must point to public template
    return render_template('public/user_signup.html')
# --- USER LOGIN ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('product.home'))  # or user dashboard
        else:
            flash('No account found, please sign up first.', 'warning')
            return redirect(url_for('auth.signup'))

    return render_template('public/user_login.html')
