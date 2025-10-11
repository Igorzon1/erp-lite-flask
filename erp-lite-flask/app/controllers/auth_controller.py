# app/controllers/auth_controller.py
from urllib.parse import urlparse, urljoin
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user
from ..models.user import User
from ..extensions import db, bcrypt

auth = Blueprint('auth', __name__)

def is_safe_url(target):
    """Verifica se 'target' é uma URL interna/segura do mesmo host."""
    host_url = request.host_url  # ex: 'http://localhost:5000/'
    ref_url = urlparse(host_url)
    test_url = urlparse(urljoin(host_url, target))
    return (test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('products.index'))  # redireciona se já estiver logado

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 1. Verifica se usuário/email já existe
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists or email_exists:
            flash('Usuário ou email já cadastrado.', 'danger')
            return redirect(url_for('auth.register'))

        # 2. Cria o novo usuário
        user = User(username=username, email=email)
        user.set_password(password)  # cria hash da senha

        db.session.add(user)
        db.session.commit()

        flash('Sua conta foi criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('products.index'))  # já logado

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # remember pode vir como 'on' ou None — convertemos para bool
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)

            # Preferimos o 'next' vindo do POST (campo hidden), se não, da query string
            next_page = request.form.get('next') or request.args.get('next')

            # Se existir e for seguro, redireciona para ele
            if next_page and is_safe_url(next_page):
                return redirect(next_page)

            # Caso contrário, redireciona para o padrão
            return redirect(url_for('products.index'))
        else:
            flash('Login Inválido. Verifique o email e a senha.', 'danger')

    # GET: renderiza template; inclua o next como hidden no form (veja login.html)
    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))
