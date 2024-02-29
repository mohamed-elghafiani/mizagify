from ..utils import db
from .base_model import BaseModel


# Define the intermediary table for the many-to-many relationship
booking_table_association = db.Table(
    'booking_table_association',
    db.Column('booking_id', db.Integer(), db.ForeignKey('bookings.id'), primary_key=True),
    db.Column('table_id', db.Integer(), db.ForeignKey('tables.id'), primary_key=True)
)


class Booking(BaseModel):
    """The Booking Data Model"""
    __tablename__ = "bookings"

    num_of_people = db.Column(db.Integer(), nullable=False)
    booking_time = db.Column(db.DateTime(), nullable=False)
    booker_first_name = db.Column(db.String(20), nullable=False)
    booker_last_name = db.Column(db.String(20), nullable=False)
    booker_email = db.Column(db.String(50), nullable=False)
    booker_phone = db.Column(db.String(15), nullable=False)
    booker_occasion = db.Column(db.String())
    booker_request = db.Column(db.Text())

    tables = db.relationship('Table', secondary=booking_table_association, backref='bookings')

    restaurant_id = db.Column(db.String(36), db.ForeignKey("restaurants.id"), nullable=False)
