# app/controllers/auth_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
# Importações ajustadas (sem 'app.' prefix)
from ..models.user import User
from ..extensions import db

# Cria o Blueprint para as rotas de autenticação
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) # Redireciona se já estiver logado
    
    # Lógica de Formulário (usando Flask-WTF, que você precisaria adicionar ao requirements.txt)
    # Por enquanto, focaremos na lógica de banco.
    
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
        user.set_password(password) # Usa a função que cria o hash

        db.session.add(user)
        db.session.commit()
        
        flash('Sua conta foi criada com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html') # Você precisará criar esse template

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) # Redireciona se já estiver logado

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') # Campo 'Lembrar de mim' (checkbox)

        user = User.query.filter_by(email=email).first()
        
        # 1. Verifica a existência e a senha
        if user and user.check_password(password):
            login_user(user, remember=remember) # Loga o usuário
            
            # Redireciona para a página de onde o usuário veio
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Inválido. Verifique o email e a senha.', 'danger')
            
    return render_template('auth/login.html') # Você precisará criar esse template


@auth.route('/logout')
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))