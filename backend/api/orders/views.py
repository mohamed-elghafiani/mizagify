from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus


orders_namespace = Namespace("orders", description="A Namespace for orders Blueprint")

order_model = orders_namespace.model(
    'Order', {
        "id": fields.Integer(description="An ID"),
        "size": fields.String(description="Size of order", required=True, 
            emun=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]
        ),
        "order_status": fields.String(description="The status of the order",
            required=True, enum=["PENDING", "IN_TRANSIT", "DELIVERED"])
    }
)

@orders_namespace.route('/')
class Order(Resource):
    """Order class
    methods:
      get: returns all orders
      post: create an order
    """
    @orders_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """Return all orders"""
        orders = Order.query.all()

        return orders, HTTPStatus.OK
    
    @orders_namespace.expect(order_model)
    @jwt_required()
    def post(self):
        """Create a new order"""
        data = orders_namespace.payload

        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        new_order = Order(
            size=data["size"],
            quantity=data["quantity"],
            flavour=data["flavour"]
        )
        new_order.customer = user.id
        new_order.save()

        return new_order, HTTPStatus.CREATED
    

@orders_namespace.route('/<int:order_id>')
class ChangeOrder(Resource):
    """GET, UPDATE, DELETE an order with the id order_id"""
    def get(self, order_id):
        """Retrieve an order by id"""
        pass

    def put(self, order_id):
        """Update an order with id"""
        pass

    def delete(self, order_id):
        """Delete an order with id"""
        pass

@orders_namespace.route("/user/<int:user_id>/<int:order_id>")
class UserOrder(Resource):
    """Retrieve the user's order by id"""
    def get(self, user_id, order_id):
        """Retrieve the user's order by id"""
        pass

@orders_namespace.route("/user/<int:user_id>/orders")
class UserOrders(Resource):
    """User orders"""
    def get(self, user_id):
        """Get all orders for a specific user with id"""
        pass

@orders_namespace.route("/status/<int:order_id>")
class UpdateOrderStatus(Resource):
    """Update order status"""
    def patch(self, order_id):
        """Update an order's status"""
        pass