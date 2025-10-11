# app/__init__.py
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, url_for, request
from flask_login import current_user
from .config import Config
from .extensions import db, login_manager, jwt, bcrypt, migrate


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_class)

    # --- Inicialização das extensões ---
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # --- Configurações do Flask-Login ---
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # --- Registro dos Blueprints ---
    from .controllers.auth_controller import auth as auth_bp
    from .controllers.product_controller import products_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/products')

    # --- Rota raiz ---
    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('products.index'))
        return redirect(url_for('auth.login'))

    # --- Proteção global: exige login em quase tudo ---
    PUBLIC_ENDPOINTS = {
        'auth.login',
        'auth.register',
        'auth.logout',
        'static',
    }

    @app.before_request
    def require_login():
        """Impede acesso de usuários não logados às rotas privadas."""
        endpoint = request.endpoint  # nome da função que está sendo chamada

        # Ignora endpoints inválidos (ex: favicon.ico)
        if endpoint is None:
            return None

        # Libera arquivos estáticos (CSS, JS, imagens)
        if endpoint.startswith('static'):
            return None

        # Libera as rotas públicas definidas
        if endpoint in PUBLIC_ENDPOINTS:
            return None

        # Em modo debug, ignora rotas internas do Flask
        if app.debug and endpoint.startswith('flask_'):
            return None

        # Se o usuário não estiver autenticado, redireciona para o login
        if not current_user.is_authenticated:
            # o "next" guarda a página que o usuário tentou acessar
            return redirect(url_for('auth.login', next=request.path))

    # --- Error handlers ---
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
