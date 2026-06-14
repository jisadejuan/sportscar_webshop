from flask import Blueprint, render_template, request
from app.models.product import Product
from app import db

product_bp = Blueprint('product', __name__)

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

# --- READ ONLY ---
@product_bp.route('/products')
def product_list():
    products = Product.query.all()
    categories = {}
    for car in products:
        categories.setdefault(car.category, []).append(car)
    return render_template('products/list.html', categories=categories)

@product_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    if product is None:
        # Kung wala ang product, ipakita na lang ulit ang list
        products = Product.query.all()
        categories = {}
        for car in products:
            categories.setdefault(car.category, []).append(car)
        return render_template('products/list.html', categories=categories)
    return render_template('products/detail.html', product=product)

@product_bp.route('/products/<int:product_id>/delete', methods=['GET', 'POST'])
def product_delete(product_id):
    product = Product.query.get(product_id)
    if product is None:
        # Kung wala ang product, balik sa list
        products = Product.query.all()
        categories = {}
        for car in products:
            categories.setdefault(car.category, []).append(car)
        return render_template('products/list.html', categories=categories)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        # Pagkatapos mag-delete, ipakita ulit ang list
        products = Product.query.all()
        categories = {}
        for car in products:
            categories.setdefault(car.category, []).append(car)
        return render_template('products/list.html', categories=categories)

    return render_template('admin/confirm_delete.html', product=product)
