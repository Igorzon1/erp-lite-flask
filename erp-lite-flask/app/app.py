from dotenv import load_dotenv
load_dotenv() 

from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from controllers.product_controller import products_bp
from db import db 

# Importa as extensões de segurança e autenticação
from flask_login import LoginManager, current_user
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Importa o Blueprint de Autenticação (que criaremos/usaremos em seguida)
from controllers.auth_controller import auth # Importa o Blueprint 'auth'

# --- 1. Inicializa as extensões de segurança ---
login_manager = LoginManager()
jwt = JWTManager()
bcrypt = Bcrypt()


# Cria e configura a aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# --- 2. Inicializa as extensões com a aplicação ---
db.init_app(app) 
login_manager.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

# Configuração do Flask-Login
# Define a view (rota) para onde o usuário deve ser redirecionado se não estiver logado
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

# --- 3. Função de User Loader para Flask-Login ---
# O Flask-Login precisa saber como recarregar um objeto User dado seu ID
from models.user import User # Importa o seu modelo User

@login_manager.user_loader
def load_user(user_id):
    # Procura e retorna o objeto User a partir do ID na sessão
    return User.query.get(int(user_id))


# Configura o local das views (templates)
app.template_folder = 'views/templates'

# --- 4. Registra os Blueprints ---
# Registra o Blueprint de Autenticação
app.register_blueprint(auth, url_prefix='/auth') 

# Registra o Blueprint do Produto
app.register_blueprint(products_bp, url_prefix='/products')

@app.route('/')
def home():
    # Rota raiz livre. Redireciona para o painel principal (dashboard) ou produtos
    if current_user.is_authenticated:
        return redirect(url_for('products.index'))
    else:
        # Se não estiver logado, redireciona para a tela de login
        return redirect(url_for('auth.login')) 


# Rota de tratamento de erro 404 (Opcional)
@app.errorhandler(404)
def page_not_found(e):
    # Certifique-se de que este template existe em views/templates/404.html
    return render_template('404.html'), 404

with app.app_context():
    # Cria todas as tabelas definidas nos seus modelos (Product e User)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)