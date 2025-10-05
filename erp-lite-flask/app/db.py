# app/db.py

from flask_sqlalchemy import SQLAlchemy

# Cria a instância do SQLAlchemy, mas NÃO a inicializa (lazy initialization)
db = SQLAlchemy()