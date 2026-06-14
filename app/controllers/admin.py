from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.admin_user import AdminUser

# Define the blueprint FIRST
admin_bp = Blueprint('admin', __name__)

# --- SIGN UP ---
@admin_bp.route('/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_admin = AdminUser.query.filter_by(email=email).first()
        if existing_admin:
            flash('Admin email already registered, please log in.', 'danger')
            return redirect(url_for('admin.admin_signup'))

        new_admin = AdminUser(email=email)
        new_admin.password = password  # simpleng save muna, walang hashing kung di pa kayo nag-aaral ng sessions/security
        db.session.add(new_admin)
        db.session.commit()

        flash('Admin signed up successfully, log in now.', 'success')
        return redirect(url_for('admin.admin_login'))

    return render_template('admin/admin_signup.html')

# --- LOGIN ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = AdminUser.query.filter_by(email=email, password=password).first()
        if admin:
            flash('Login successful!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('admin/admin_login.html')

# --- DASHBOARD ---
@admin_bp.route('/dashboard')
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')
