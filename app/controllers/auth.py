from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User
from app.models.admin_user import AdminUser

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# User login
@auth_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check user by email + password
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('User login successful!', 'success')
            return redirect(url_for('product.product_list'))
        else:
            flash('Invalid user credentials', 'danger')
    return render_template('public/login.html')

# Admin login
@auth_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = AdminUser.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_id'] = admin.id
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    return render_template('auth/admin_login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('auth.user_login'))

        # Create new user
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Automatically log in the new user
        session['user_id'] = new_user.id
        flash('Account created successfully! Welcome!', 'success')

        # Redirect straight to home (user-only page)
        return redirect(url_for('product.product_list'))

    return render_template('public/register.html')
