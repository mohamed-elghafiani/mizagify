from ..utils import db
from enum import Enum
from .base_model import BaseModel


class Price(Enum):
    """Restaurant Prices"""
    CHEAP = 'cheap'
    REGULAR = 'regular'
    EXPENSIVE = 'expensive'

class ImageType(Enum):
    """Image Types"""
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Restaurant(BaseModel):
    """Restaurant Model"""
    __tablename__ = "restaurants"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    open_time = db.Column(db.Time(), nullable=False)
    close_time = db.Column(db.Time(), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Enum(Price), nullable=False)
    # location = db.Column(db.Text(), nullable=False)
    images = db.Column(db.Text(), nullable=False)
    
    reviews = db.relationship('Review', backref="restaurant", lazy=True)
    items = db.relationship('Item', backref="restaurant", lazy=True)
    tables = db.relationship("Table", backref="restaurant", lazy=True)
    bookings = db.relationship("Booking", backref="restaurant", lazy=True)

    location_id = db.Column(db.String(36), db.ForeignKey("locations.id"), nullable=False)
    cuisine_id = db.Column(db.String(36), db.ForeignKey("cuisines.id"), nullable=False)


class Table(BaseModel):
    """Table Model"""
    __tablename__ = "tables"

    name = db.Column(db.String(), nullable=False)
    seats = db.Column(db.Integer(), nullable=False)
    restaurant_id = db.Column(db.String(36), db.ForeignKey("restaurants.id"), nullable=False)


class Item(BaseModel):
    """Item Model"""
    __tablename__ = "items"

    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    restaurant_id = db.Column(db.String(36), db.ForeignKey("restaurants.id"), nullable=False)


class Cuisine(BaseModel):
    """Cuisine Model"""
    __tablename__ = "cuisines"

    name = db.Column(db.String(100), nullable=False, unique=True)
    restaurants = db.relationship('Restaurant', backref="cuisine", lazy=True)


# class Image(BaseModel):
#     """Image Model"""
#     __tablename__ = "images"

#     url = db.Column(db.Text(), nullable=False)
#     type = db.Column(db.Enum(ImageType), nullable=False)
#     restaurant_id = db.Column(db.String(36), db.ForeignKey("restaurants.id"), nullable=False)


class Location(BaseModel):
    """Location Model"""
    __tablename__ = "locations"
    
    name = db.Column(db.Text(), nullable=False, unique=True)
    restaurants = db.relationship('Restaurant', backref="location", lazy=True)