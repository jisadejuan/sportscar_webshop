from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.admin import Admin
from app.models.product import Product

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
            session['admin_id'] = admin.id
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('No admin account found, please sign up first.', 'warning')
            return redirect(url_for('admin.admin_signup'))

    # GET request → unified login page
    return render_template('public/login.html')
# --- ADMIN DASHBOARD ---
@admin_bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:   # 👉 check kung naka-login
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin.admin_login'))

    products = Product.query.all()
    return render_template('admin/admin.html', products=products)

# --- CREATE PRODUCT ---
@admin_bp.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if 'admin_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin.admin_login'))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        new_product = Product(name=name, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/create_product.html')

# --- EDIT PRODUCT ---
@admin_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'admin_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin.admin_login'))

    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_product.html', product=product)

# --- DELETE PRODUCT ---
@admin_bp.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'admin_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin.admin_login'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# --- ADMIN LOGOUT ---
@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)   # 👉 clear session
    flash('Logged out successfully.', 'success')
    return redirect(url_for('admin.login'))
