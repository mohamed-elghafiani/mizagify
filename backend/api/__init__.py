from flask import Flask
from .config import config_dict
from .utils import db
from .models.user import User
from .models.order import Order
from .models.booking import Booking, booking_table_association
from .models.restaurant import Restaurant, Item, Cuisine, Location
from .models.review import Review
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .api import api
from flask_cors import CORS, cross_origin


def create_app(config=config_dict["dev"]):
    """Create a flask app"""
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)

    CORS(app, supports_credentials=True)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # @app.after_request
    # def middleware_for_response(response):
    #     response.headers.add('Access-Control-Allow-Credentials', 'true')
    #     return response

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order,
            'Booking': Booking,
            'Restaurant': Restaurant,
            'Item': Item,
            'Cuisine': Cuisine,
            'Review': Review,
            "Location": Location,
            "Booking_Table_Association": booking_table_association
        }

    return app