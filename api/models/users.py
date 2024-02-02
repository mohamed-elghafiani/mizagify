from ..utils import db


class User(db.Model):
    """User class"""
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    is_staff = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def save(self):
        """Save user data to database"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<User {self.username}>"