from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app.models_admin.admin_user import AdminUser
from app import db_user, db_admin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# User login
@auth_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
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
