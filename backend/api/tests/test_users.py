import unittest
from .. import create_app
from ..config import config_dict
from ..utils import db
from ..models.user import User


class TestUser(unittest.TestCase):
    """User Test Class"""
    def setUp(self):
        """SetUp method"""
        self.app = create_app(config=config_dict["test"])

        self.appcntx = self.app.app_context()
        self.appcntx.push()

        self.client = self.app.test_client()
        db.create_all()

    def test_user_registration(self):
        """Test user registration"""
        data = {
            "username": "testuser",
            "email": "test@email.com",
            "password": "test123"
        }
        response = self.client.post("/auth/signup", json=data)
        user = User.query.filter_by(email=data["email"]).first()

        assert user.username == data["username"]
        assert response.status_code == 201

    def test_user_login(self):
        """Test user login"""
        data = {
            "email": "test@email.com",
            "password": "test123"
        }
        response = self.client.post("/auth/login", json=data)

        # Assert user not found
        assert response.status_code == 400

    def tearDown(self):
        """Tear Down method"""
        db.drop_all()
        self.appcntx.pop()
        self.app = None
        self.client = None