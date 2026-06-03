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

@product_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail.html', product=product)

# --- CREATE ---------------------------------------------------------------
@product_bp.route('/products/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')
        image = request.form.get('image')

        # Validate — make sure required fields are not empty
        if not name or not category or not price:
            flash('Name, category, and price are required.', 'error')
            return redirect(url_for('product.create_product'))

        # Create the new Product object and save it
        new_product = Product(
            name=name,
            category=category,
            price=float(price),
            stock=int(stock) if stock else 0,
            description=description,
            image=image
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('product.product_list'))

    # GET request — show the empty form
    return render_template('products/create.html')
# --- UPDATE ---
@product_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.category = request.form.get('category')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.description = request.form.get('description')
        product.image = request.form.get('image')

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product.product_list'))

    return render_template('products/edit.html', product=product)

# --- DELETE ---
@product_bp.route('/products/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
        return redirect(url_for('product.product_list'))

    return render_template('products/confirm_delete.html', product=product)
