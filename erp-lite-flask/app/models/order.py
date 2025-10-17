import uuid
from datetime import datetime
from app.extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    client_id = db.Column(db.String(36), db.ForeignKey('clients.id', ondelete='SET NULL'), nullable=True, index=True)
    status = db.Column(db.String(50), nullable=False, default='draft')  # draft, confirmed, shipped, cancelled, etc.
    total = db.Column(db.Numeric(12, 2), nullable=True, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = db.relationship('Client', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    def recalc_total(self):
        self.total = sum([(item.unit_price * item.quantity) for item in self.items])

    def __repr__(self):
        return f'<Order {self.id} status={self.status} total={self.total}>'
