import uuid
from datetime import datetime
from enum import Enum
from app.extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class MovementType(Enum):
    IN = 'entrada'
    OUT = 'saida'
    RESERVE = 'reserva'
    RELEASE = 'reversao'  # reversão de reserva/cancelamento

# Lote físico -> referencia o produto e local fisico
class InventoryBatch(db.Model):
    __tablename__ = 'inventory_batches'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    lot = db.Column(db.String(120), nullable=True)               # número do lote (opcional)
    expiry_date = db.Column(db.Date, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)  # quantidade atual no lote
    stock_location_id = db.Column(db.String(36), db.ForeignKey('stock_locations.id', ondelete='SET NULL'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', back_populates='batches')
    stock_location = db.relationship('StockLocation', back_populates='batches')
    movements = db.relationship('InventoryMovement', back_populates='batch', cascade='all, delete-orphan')

    def adjust_quantity(self, delta, session=None):
        """Ajusta quantidade (positivo para entrada, negativo para saída).
           Preferência por usar transação / service para gravar movement + ajuste."""
        self.quantity = (self.quantity or 0) + int(delta)
        if self.quantity < 0:
            raise ValueError('Quantidade do lote não pode ficar negativa via adjust_quantity.')
        if session:
            session.add(self)

    def __repr__(self):
        return f'<InventoryBatch {self.id} product={self.product_id} qty={self.quantity}>'

class InventoryMovement(db.Model):
    __tablename__ = 'inventory_movements'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    batch_id = db.Column(db.String(36), db.ForeignKey('inventory_batches.id', ondelete='CASCADE'), nullable=False, index=True)
    type = db.Column(db.String(30), nullable=False)   # usar valores de MovementType
    quantity = db.Column(db.Integer, nullable=False)
    document_id = db.Column(db.String(36), nullable=True)   # pode referenciar order id, nota fiscal, etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    batch = db.relationship('InventoryBatch', back_populates='movements')

    def __repr__(self):
        return f'<InventoryMovement {self.type} {self.quantity} batch={self.batch_id}>'
