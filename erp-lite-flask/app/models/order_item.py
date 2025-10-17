import uuid
from decimal import Decimal
from app.extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id', ondelete='SET NULL'), nullable=True, index=True)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False, default=Decimal('0.00'))

    # referência opcional para lote alocado (quando precisar reservar/associar um lote físico)
    batch_allocated = db.Column(db.String(36), db.ForeignKey('inventory_batches.id', ondelete='SET NULL'), nullable=True)

    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')
    allocated_batch = db.relationship('InventoryBatch', foreign_keys=[batch_allocated])

    def line_total(self):
        return self.unit_price * self.quantity

    def __repr__(self):
        return f'<OrderItem {self.id} product={self.product_id} qty={self.quantity}>'
