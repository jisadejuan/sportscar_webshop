from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.product import Product

product_bp = Blueprint('product', __name__)

# --- STATIC PAGES ---
@product_bp.route('/')
def home():
    return render_template('public/index.html')

@product_bp.route('/about')
def about():
    return render_template('public/about.html')

@product_bp.route('/contact')
def contact():
    return render_template('public/contact.html')

@product_bp.route('/login')
def login():
    return render_template('public/login.html')

@product_bp.route('/categories')
def categories():
    return render_template('public/categories.html')

# --- READ ---
@product_bp.route('/products')
def product_list():
    products = Product.query.all()
    categories = {}
    for car in products:
        categories.setdefault(car.category, []).append(car)
    return render_template('products/list.html', categories=categories)

@product_bp.route('/admin')
def admin_dashboard():
    products = Product.query.all()
    return render_template('admin/admin.html', products=products)

@product_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail.html', product=product)

# --- CREATE ---------------------------------------------------------------
@product_bp.route('/admin/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name        = request.form.get('name')
        category    = request.form.get('category')
        price       = request.form.get('price')
        stock       = request.form.get('stock')
        description = request.form.get('description')
        image       = request.form.get('image')

        # Validate required fields
        if not name or not category or not price or not stock:
            return redirect(url_for('product.create_product'))

        # Create and save new product
        new_product = Product(
            name=name,
            category=category,
            price=price,
            stock=stock,
            description=description,
            image=image
        )
        from app import db
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('product.admin_dashboard'))

    # GET — show empty form
    return render_template('admin/create.html')


# --- DELETE ---------------------------------------------------------------
@product_bp.route('/admin/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if product is None:
        return redirect(url_for('product.admin_dashboard'))

    if request.method == 'POST':
        from app import db
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('product.admin_dashboard'))

    # GET — show confirm delete form
    return render_template('admin/confirm_delete.html', product=product)

# --- UPDATE ---
@product_bp.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)

    if product is None:
        # Instead of flash, just redirect if not found
        return redirect(url_for('product.admin_dashboard'))

    if request.method == 'POST':
        name        = request.form.get('name')
        category    = request.form.get('category')
        price       = request.form.get('price')
        stock       = request.form.get('stock')
        description = request.form.get('description')
        image       = request.form.get('image')

        # Simple validation
        if not name or not category or not price or not stock:
            return redirect(url_for('product.edit_product', product_id=product_id))

        # Update attributes
        product.name        = name
        product.category    = category
        product.price       = price
        product.stock       = stock
        product.description = description
        product.image       = image

        # Persist changes to MariaDB
        from app import db
        db.session.commit()

        return redirect(url_for('product.admin_dashboard'))

    # GET - show pre-filled form
    return render_template('admin/edit.html', product=product)
    
# --- DELETE ---
@product_bp.route('/admin/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        # Normally you'd delete from DB here, but session is removed
        flash('Product deleted successfully! (DB delete skipped)', 'success')
        return redirect(url_for('product.admin_dashboard'))

    return render_template('admin/confirm_delete.html', product=product)
