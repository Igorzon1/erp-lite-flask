import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()
class Config:
    # ... (outras configurações)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_secreta_muito_forte_aqui'
    DEBUG = True

    # Use a variável de ambiente DATABASE_URL que conterá o link do Supabase
    # Exemplo (você deve definir esta variável no seu ambiente):
    # export DATABASE_URL='postgresql://[usuário]:[senha]@[host]:[porta]/[nome_bd]'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///site.db' # Fallback para SQLite
    
    # Configurações do JWT e Bcrypt
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'sua_chave_jwt_muito_forte' 

    
    SQLALCHEMY_TRACK_MODIFICATIONS = False