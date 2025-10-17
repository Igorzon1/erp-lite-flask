import uuid
from datetime import datetime
from app.extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(200), nullable=False)
    cpf_cnpj = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relacionamento para endereço (um cliente pode ter vários endereços)
    addresses = db.relationship('Address', back_populates='client', cascade='all, delete-orphan')

    orders = db.relationship('Order', back_populates='client')

    def __repr__(self):
        return f'<Client {self.name}>'
