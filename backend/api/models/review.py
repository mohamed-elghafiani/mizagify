from base_model import BaseModel
from ..utils import db


class Review(BaseModel):
    """Review Model"""
    __tablename__ = "reviews"

    text = db.Column(db.Text(), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    restaurant_id = db.Column(db.String(36), db.ForeignKey("restaurants.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)