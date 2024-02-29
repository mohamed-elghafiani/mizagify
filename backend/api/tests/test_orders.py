import unittest
from .. import create_app
from ..utils import db
from ..config import config_dict
from flask_jwt_extended import create_access_token


class TestOrder(unittest.TestCase):
    """Orders Test Class"""
    def setUp(self):
        """SetUp method"""
        self.app = create_app(config=config_dict["test"])
        self.appcntx = self.app.app_context()
        self.appcntx.push()
        self.client = self.app.test_client()
        db.create_all()

    def test_get_all_orders(self):
        """Test GET all orders"""
        token = create_access_token(identity="testuser")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get("/orders/", headers=headers)

        assert response.status_code == 200
        assert response.json == []

    def test_create_order(self):
        """Test create order"""
        # Create a user
        data = {
            "username": "testuser",
            "email": "test@email.com",
            "password": "test123"
        }
        response = self.client.post("/auth/signup", json=data)

        # Login user and get jwt token
        data = {
            "email": "test@email.com",
            "password": "test123"
        }
        response = self.client.post("/auth/login", json=data)
        token = response.json["access_token"]
        
        # token = create_access_token(identity="testuser")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        data = {
            "size": "SMALL",
            "flavour": "Test Flavour"
        }
        response = self.client.post("/orders/", json=data, headers=headers)

        assert response.status_code == 201

    def tearDown(self):
        """TearDown Method"""
        db.drop_all()
        self.appcntx.pop()
        self.app = None
        self.client = None