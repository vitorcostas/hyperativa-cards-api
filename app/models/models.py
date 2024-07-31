from datetime import datetime
import uuid
from app import db


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    insertion_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cards = db.relationship('Card', backref='owner', lazy=True)


class Card(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    card_number = db.Column(db.BigInteger, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    insertion_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)