from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.product import Product
from app import db

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

@product_bp.route('/admin/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        stock = request.form['stock']
        description = request.form['description']
        image = request.form['image']

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

        flash('Product created successfully!', 'success')
        return redirect(url_for('product.admin_dashboard'))

    # Render the correct template path
    return render_template('admin/create.html')
    
# --- UPDATE ---------------------------------------------------------------
@product_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)

    if product is None:
        flash('Product not found.', 'error')
        return redirect(url_for('product.product_list'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')
        image = request.form.get('image')

        # Validate — make sure required fields are not empty
        if not name or not category or not price:
            flash('All fields are required.', 'error')
            return redirect(url_for('product.edit_product', product_id=product_id))

        # Update the existing record's attributes
        product.name = name
        product.category = category
        product.price = float(price)
        product.stock = int(stock) if stock else 0
        product.description = description
        product.image = image

        db.session.commit()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('product.product_list'))

    # GET — show the pre-filled edit form
    return render_template('products/edit.html', product=product)
    
# --- DELETE ---------------------------------------------------------------
@product_bp.route('/admin/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
        return redirect(url_for('product.admin_dashboard'))

    # FIXED TEMPLATE PATH
    return render_template('admin/confirm_delete.html', product=product)
