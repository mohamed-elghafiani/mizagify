from ..utils import db
from .base_model import BaseModel


class User(BaseModel):
    """User class"""
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String())
    password_hash = db.Column(db.Text(), nullable=False)
    city = db.Column(db.String(50))
    # role = db.Column(db.String(), default="user")
    # bookings = db.relationship('', backref='customer', lazy=True)