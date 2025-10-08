# app/__init__.py
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, url_for
from .config import Config  # ou importe do caminho correto
from .extensions import db, login_manager, jwt, bcrypt, migrate

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_class)

    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Configurações do Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Registra blueprints (import local para evitar circular)
    from .controllers.auth_controller import auth as auth_bp
    from .controllers.product_controller import products_bp as products_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/products')

    # rota raiz
    @app.route('/')
    def home():
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('products.index'))
        return redirect(url_for('auth.login'))

    # Error handlers (exemplo)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Se quiser criar tabelas automaticamente em dev:
    # with app.app_context():
    #     db.create_all()

    return app
