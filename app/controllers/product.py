from flask import Blueprint, render_template, request
from app.models.product import Product

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
    items = Product.query.all()
    categories = {}
    for car in items:
        categories.setdefault(car.category, []).append(car)
    return render_template('products/list.html', categories=categories)

@product_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    item = Product.query.get(product_id)
    if item is None:
        # Kung wala ang product, ipakita na lang ulit ang list
        items = Product.query.all()
        categories = {}
        for car in items:
            categories.setdefault(car.category, []).append(car)
        return render_template('products/list.html', categories=categories)
    return render_template('products/detail.html', item=item)

# --- SEARCH ---
@product_bp.route('/products/search')
def search():
    query = request.args.get('q', '')  # kunin ang input mula sa search bar
    if not query:
        # kung walang laman, ipakita lahat ng products
        items = Product.query.all()
    else:
        # hanapin yung mga products na kapareho o malapit ang pangalan
        items = Product.query.filter(Product.name.ilike(f"%{query}%")).all()

    categories = {}
    for car in items:
        categories.setdefault(car.category, []).append(car)

    return render_template('products/list.html', categories=categories, search=query)
