from ..utils import db
from base_model import BaseModel


class Booking(BaseModel):
    """The Booking Data Model"""
    __tablename__ = "bookings"

    id = db.Column(db.Integer(), primary_key=True)
    num_of_people = db.Column(db.Integer(), nullable=False)
    booking_time = db.Column(db.DateTime(), nullable=False)
    booker_first_name = db.Column(db.String(20), nullbale=False)
    booker_last_name = db.Column(db.String(20), nullbale=False)
    booker_email = db.Column(db.String(50), nullable=False)
    booker_phone = db.Column(db.String(15), nullable=False)
    booker_occasion = db.Column(db.String())
    booker_request = db.Column(db.Text())

