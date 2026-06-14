from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.admin import Admin

admin_bp = Blueprint('admin', __name__)

# --- ADMIN SIGN UP ---
@admin_bp.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            flash('Admin account already exists, please log in.', 'danger')
            return redirect(url_for('admin.admin_login'))

        new_admin = Admin(email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()

        flash('Admin account signed up successfully!', 'success')
        return redirect(url_for('admin.admin_login'))

    return render_template('admin/admin_signup.html')

# --- ADMIN LOGIN ---
@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = Admin.query.filter_by(email=email, password=password).first()
        if admin:
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin.dashboard'))  # or admin dashboard
        else:
            flash('No admin account found, please sign up first.', 'warning')
            return redirect(url_for('admin.admin_signup'))

    return render_template('admin/admin_login.html')
