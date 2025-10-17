import uuid
from datetime import datetime
from app.extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    client_id = db.Column(db.String(36), db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    street = db.Column(db.String(300))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zip = db.Column(db.String(40))
    country = db.Column(db.String(100), default='BR')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', back_populates='addresses')

    def __repr__(self):
        return f'<Address {self.id} - {self.city}>'
