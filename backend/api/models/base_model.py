from ..utils import db
from datetime import datetime
from uuid import uuid4


class BaseModel(db.Model):
    """Base Model"""
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

    # def __init__(self, **kwargs):
    #     """Object initiator"""
    #     for key, val, in kwargs:
    #         setattr(self, key, val)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"
    
    @classmethod
    def get_by_id(cls, id):
        """Get object by id"""
        return cls.query.get_or_404(id)

    def save(self):
        """Save order to database"""
        db.session.add(self)
        db.session.commit()

    def commit(self):
        """Commit to database"""
        db.session.commit()

    def delete(self):
        """Delete from database"""
        db.session.delete(self)
        db.session.commit()