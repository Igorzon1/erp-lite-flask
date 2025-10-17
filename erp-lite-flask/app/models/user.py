# app/models/user.py
from flask_login import UserMixin
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager,bcrypt

def gen_uuid():
    return str(uuid.uuid4())

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    _password_hash = db.Column('password_hash', db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # senha via property (hash)
    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, plain):
        self._password_hash = bcrypt.generate_password_hash(plain).decode('utf-8')

    def check_password(self, plain):
        return bcrypt.check_password_hash(self._password_hash, plain)

    def __repr__(self):
        return f'<User {self.username}>'

# user_loader — colocado aqui porque importamos login_manager das extensions (não do app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))