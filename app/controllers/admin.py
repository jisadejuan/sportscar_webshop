from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.product import Product
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Dashboard
@admin_bp.route('/')
def admin_dashboard():
    products = Product.query.all()
    return render_template('admin/admin.html', products=products)

# Create
@admin_bp.route('/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        new_product = Product(
            name=request.form['name'],
            category=request.form['category'],
            price=request.form['price'],
            stock=request.form['stock'],
            description=request.form['description'],
            image=request.form['image']
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/create.html')

# Edit
@admin_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.description = request.form['description']
        product.image = request.form['image']
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/edit.html', product=product)

# Delete
@admin_bp.route('/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/confirm_delete.html', product=product)
