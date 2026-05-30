from flask import Blueprint, render_template
from app.models.product import Product

product_bp = Blueprint('product', __name__)

@product_bp.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@product_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    return render_template('products/detail.html', product=product)
