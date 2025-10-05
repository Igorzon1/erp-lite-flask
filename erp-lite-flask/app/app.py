from dotenv import load_dotenv
# ==========================================================
# 1. Carrega as variáveis do arquivo .env (deve estar na raiz do projeto)
# ==========================================================
load_dotenv() 

from flask import Flask, render_template, redirect, url_for
from config import Config
# Importação do Blueprint (que agora não gera mais o ciclo)
from controllers.product_controller import products_bp
# NOVO: Importa 'db' do seu novo arquivo de extensão
from db import db 


# Cria e configura a aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# ==========================================================
# 2. Inicializa o banco de dados com o objeto 'app'
# ==========================================================
db.init_app(app) 

# Configura o local das views (templates)
app.template_folder = 'views/templates'

# Registra o Blueprint do Produto
app.register_blueprint(products_bp, url_prefix='/products')

@app.route('/')
def home():
    # Rota raiz livre, redireciona para a lista de produtos
    return redirect(url_for('products.index'))

# Rota de tratamento de erro 404 (Opcional)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ==========================================================
# 3. Criação das tabelas (com o contexto da aplicação)
# Deve ser executado ANTES de rodar o app para criar as tabelas
# no Supabase/SQLite.
# ==========================================================
with app.app_context():
    # Cria todas as tabelas definidas nos seus modelos (Product)
    db.create_all()

if __name__ == '__main__':
    app.run()