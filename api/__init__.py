from flask import Flask
from .auth.views import auth_namespace
from .orders.views import orders_namespace
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.users import User
from .models.orders import Order
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(config=config_dict["dev"]):
    """Create a flask app"""
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    api = Api(app)
    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(orders_namespace, path="/orders")

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order
        }

    return app