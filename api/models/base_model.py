from ..utils import db
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from uuid import uuid4


class BaseModel(db.Model):
    """Base Model"""
    __abstract__ = True

    id = Column(String(60), primary_key=True, nullable=False, unique=True, default=str(uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"
    
    def save(self):
        """Save order to database"""
        db.session.add(self)
        db.session.commit()