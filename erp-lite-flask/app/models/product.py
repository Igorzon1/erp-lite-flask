import uuid
from datetime import datetime
from app.extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    sku = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    weight = db.Column(db.Float, nullable=True)           # em kg por unidade
    dimensions = db.Column(db.String(120), nullable=True) # e.g. "10x5x2 cm"
    price = db.Column(db.Numeric(12, 2), nullable=True)
    class_abc = db.Column(db.String(1), nullable=True)    # A/B/C
    perishable = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship com lotes (InventoryBatch)
    batches = db.relationship('InventoryBatch', back_populates='product', cascade='all, delete-orphan')

    order_items = db.relationship('OrderItem', back_populates='product')

    def total_stock_quantity(self):
        """Soma a quantidade de todos os lotes disponíveis"""
        return sum((b.quantity for b in self.batches), 0)

    def __repr__(self):
        return f'<Product {self.sku} - {self.name}>'
