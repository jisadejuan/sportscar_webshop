from flask import Blueprint, render_template, request, redirect, url_for, session
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
            return redirect(url_for('admin.admin_login'))

        new_admin = Admin(email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()
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
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('admin.admin_signup'))

    # GET request → unified login page
    return render_template('public/login.html')

# --- ADMIN DASHBOARD ---
@admin_bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))

    products = Product.query.all()
    return render_template('admin/admin.html', products=products)

# --- CREATE PRODUCT ---
@admin_bp.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')
        image = request.form.get('image')

        new_product = Product(
            name=name,
            category=category,
            price=price,
            stock=stock,
            description=description,
            image=image
        )

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create.html')


# --- EDIT PRODUCT ---
@admin_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form.get('name', product.name)
        product.category = request.form.get('category', product.category)
        product.price = request.form.get('price', product.price)
        product.stock = request.form.get('stock', product.stock)
        product.description = request.form.get('description', product.description)
        product.image = request.form.get('image', product.image)

        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit.html', product=product)

# --- DELETE PRODUCT (with confirmation) ---
@admin_bp.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    # GET request → show confirm delete page
    return render_template('admin/confirm_delete.html', product=product)

# --- ADMIN LOGOUT ---
@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)   # 👉 clear session
    return redirect(url_for('admin.admin_login'))


@admin_bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))
    # ipakita lang ang dashboard page
    return render_template('admin/dashboard.html')

# --- VIEWING OF PRODUCTS ---

@admin_bp.route('/dashboard/products')
def dashboard_products():
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))
    items = Product.query.all()
    categories = {}
    for car in items:
        categories.setdefault(car.category, []).append(car)
    return render_template('products/list.html', categories=categories)

@admin_bp.route('/dashboard/products/<int:product_id>')
def dashboard_product_detail(product_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin.admin_login'))
    item = Product.query.get_or_404(product_id)
    return render_template('products/detail.html', item=item)
