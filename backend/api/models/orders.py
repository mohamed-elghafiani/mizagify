from ..utils import db
from enum import Enum
from datetime import datetime


class Sizes(Enum):
    """Sizes class"""
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    EXTRA_LARGE = 'extra_large'


class OrderStatus(Enum):
    """OrderStatus class"""
    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'


class Order(db.Model):
    """Order ORM class"""
    __tablename__ = "orders"

    id = db.Column(db.Integer(), primary_key=True)
    size = db.Column(db.Enum(Sizes), default=Sizes.SMALL)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    flavour = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    user = db.Column(db.Integer(), db.ForeignKey('users.id'))