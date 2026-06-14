from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models_admin.admin_product import AdminProduct
from app import db_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Dashboard
@admin_bp.route('/')
def admin_dashboard():
    products = AdminProduct.query.all()
    return render_template('admin/admin.html', products=products)

# Create
@admin_bp.route('/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        new_product = AdminProduct(
            name=request.form['name'],
            category=request.form['category'],
            price=request.form['price'],
            stock=request.form['stock'],
            description=request.form['description'],
            image=request.form['image']
        )
        db_admin.session.add(new_product)
        db_admin.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/create.html')

# Edit
@admin_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = AdminProduct.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.description = request.form['description']
        product.image = request.form['image']
        db_admin.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/edit.html', product=product)

# Delete
@admin_bp.route('/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = AdminProduct.query.get_or_404(product_id)
    if request.method == 'POST':
        db_admin.session.delete(product)
        db_admin.session.commit()
        flash('Product deleted successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/confirm_delete.html', product=product)
