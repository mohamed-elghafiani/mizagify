from ..utils import db
from enum import Enum
from base_model import BaseModel


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
    open_time = db.Column(db.DateTime(), nullable=False)
    close_time = db.Column(db.DateTime(), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Enum(Price), nullable=False)
    
    items = db.relationship('Item', backref="restaurant", lazy=True)
    images = db.relationship('Image', backref="restaurant", lazy=True)

    location_id = db.Column(db.String(36), db.ForeignKey("locations.id"), nullable=False)
    cuisine_id = db.Column(db.String(36), db.ForeignKey("cuisines.id"), nullable=False)


class Item(BaseModel):
    """Item Model"""
    __abstract__ = "items"

    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    restaurant_id = db.Column(db.String(36), db.ForeignKey("restaurants.id"), nullable=False)


class Location(BaseModel):
    """Location Model"""
    __tablename__ = "locations"
    
    name = db.Column(db.Text(), nullable=False)
    restaurants = db.relationship('Restaurant', backref="location", lazy=True)


class Cuisine(BaseModel):
    """Cuisine Model"""
    __tablename__ = "cuisines"

    name = db.Column(db.String(100), nullable=False)
    restaurants = db.relationship('Restaurant', backref="cuisine", lazy=True)


class Image(BaseModel):
    """Image Model"""
    __tablename__ = "images"

    url = db.Column(db.Text(), nullable=False)
    type = db.Column(db.Enum(ImageType), nullable=False)