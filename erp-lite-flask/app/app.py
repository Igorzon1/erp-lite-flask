from flask import Flask, render_template, redirect, url_for
from config import Config
from controllers.product_controller import products_bp

# Cria e configura a aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Configura o local das views (templates)
app.template_folder = 'views/templates'

# ==========================================================
# >>> NOVO: Registra o Blueprint com o prefixo '/products'
# Isso garante que todas as rotas de produto comecem com /products/
# ==========================================================
app.register_blueprint(products_bp, url_prefix='/products')

# ==========================================================
# >>> NOVO: Rota inicial (livre)
# Redireciona a rota '/' para a lista de produtos (exemplo)
# ==========================================================
@app.route('/')
def home():
    return redirect(url_for('products.index')) # Redireciona para /products/


# Rota de tratamento de erro 404 (Opcional)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Adicionando alguns dados iniciais de exemplo
    from models.product import Product
    Product('Laptop', 1200.00, 'Notebook de alta performance.').save()
    Product('Mouse sem Fio', 25.50, 'Mouse ergonômico e silencioso.').save()

    app.run()