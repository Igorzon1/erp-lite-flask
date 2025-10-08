# app/models/product.py
from app.extensions import db
from sqlalchemy import Column, Integer, String, Float

class Product(db.Model):
    # Define o nome da tabela no banco de dados
    __tablename__ = 'products' 

    # Colunas da tabela
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
    
    def __repr__(self):
        return f"Product('{self.name}', {self.price})"

    # ==========================================================
    # Métodos estáticos para o CRUD (Model layer)
    # ==========================================================
    @staticmethod
    def all():
        return Product.query.all()

    @staticmethod
    def get(product_id):
        # O .get() do SQLAlchemy busca pelo ID da chave primária
        return Product.query.get(product_id)

    def save(self):
        # CREATE (adiciona na sessão e commita)
        db.session.add(self)
        db.session.commit()

    def update(self, name, price, description):
        # UPDATE (o objeto já está na sessão, basta commitar)
        self.name = name
        self.price = price
        self.description = description
        db.session.commit()

    def delete(self):
        # DELETE (remove da sessão e commita)
        db.session.delete(self)
        db.session.commit()