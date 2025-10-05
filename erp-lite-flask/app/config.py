import os

class Config:
    # ... (outras configurações)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_secreta_muito_forte_aqui'
    DEBUG = True

    # Use a variável de ambiente DATABASE_URL que conterá o link do Supabase
    # Exemplo (você deve definir esta variável no seu ambiente):
    # export DATABASE_URL='postgresql://[usuário]:[senha]@[host]:[porta]/[nome_bd]'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///site.db' # Fallback para SQLite
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False