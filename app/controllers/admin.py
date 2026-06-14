from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.admin_user import AdminUser

# Define the blueprint FIRST
admin_bp = Blueprint('admin', __name__)

# --- ADMIN SIGN UP ---
@admin_bp.route('/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_admin = AdminUser.query.filter_by(email=email).first()
        if existing_admin:
            flash('Admin account already exists, please log in.', 'danger')
            return redirect(url_for('admin.admin_login'))

        new_admin = AdminUser(email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()

        flash('Admin account signed up successfully!', 'success')
        return redirect(url_for('admin.admin_login'))

    # ✅ Correct template for admin
    return render_template('admin/admin_signup.html')

# --- ADMIN LOGIN ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = AdminUser.query.filter_by(email=email, password=password).first()
        if admin:
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('No admin account found, please sign up first.', 'warning')
            return redirect(url_for('admin.admin_signup'))

    return render_template('admin/admin_login.html')

# --- ADMIN DASHBOARD ---
@admin_bp.route('/dashboard')
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')
