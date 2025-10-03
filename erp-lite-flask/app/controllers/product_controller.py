# controllers/product_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.product import Product

# Cria um Blueprint para organizar as rotas
products_bp = Blueprint('products', __name__)

# --- Rota para LISTAR todos os produtos (READ ALL) ---
@products_bp.route('/', methods=['GET'])
def index():
    products = Product.all()
    return render_template('products/index.html', products=products)

# --- Rota para EXIBIR um produto específico (READ ONE) ---
@products_bp.route('/<int:product_id>')
def show(product_id):
    product = Product.get(product_id)
    if product is None:
        flash('Produto não encontrado.', 'danger')
        return redirect(url_for('products.index'))
    return render_template('products/show.html', product=product)

# --- Rotas para CRIAR um novo produto (CREATE) ---
@products_bp.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        
        new_product = Product(name, price, description)
        new_product.save()
        
        flash(f'Produto "{name}" criado com sucesso!', 'success')
        return redirect(url_for('products.index'))
    
    return render_template('products/create.html')

# --- Rotas para EDITAR um produto (UPDATE) ---
@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.get(product_id)
    if product is None:
        flash('Produto não encontrado.', 'danger')
        return redirect(url_for('products.index'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        
        product.update(name, price, description)
        
        flash(f'Produto "{name}" atualizado com sucesso!', 'success')
        return redirect(url_for('products.show', product_id=product.id))
    
    return render_template('products/edit.html', product=product)

# --- Rota para DELETAR um produto (DELETE) ---
@products_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete(product_id):
    product = Product.get(product_id)
    if product:
        product_name = product.name
        product.delete()
        flash(f'Produto "{product_name}" removido com sucesso!', 'success')
    else:
        flash('Produto não encontrado.', 'danger')

    return redirect(url_for('products.index'))