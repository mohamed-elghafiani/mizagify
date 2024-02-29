from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.order import Order
from ..models.user import User
from http import HTTPStatus


orders_namespace = Namespace("orders", description="A Namespace for orders Blueprint")

order_model = orders_namespace.model(
    'Order', {
        "id": fields.String(description="An ID"),
        "flavour": fields.String(description="The flavour"),
        "size": fields.String(description="Size of order", required=True, 
            emun=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]
        ),
        "order_status": fields.String(description="The status of the order",
            required=True, enum=["PENDING", "IN_TRANSIT", "DELIVERED"]),
        "user_id": fields.String(description="The user ID")
    }
)

order_status_model = orders_namespace.model(
    'OrderStatus', {
        'order_status': fields.String(description="Order Status", required=True,
            enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']
        )
    }
)


@orders_namespace.route('/')
class OrderGetCreate(Resource):
    """Order class
    methods:
      get: returns all orders
      post: create an order
    """
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description="Retrieve all the orders"
    )
    @jwt_required()
    def get(self):
        """Return all orders"""
        orders = Order.query.all()

        return orders, HTTPStatus.OK
    
    @orders_namespace.expect(order_model)
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description="Place an order"
    )
    @jwt_required()
    def post(self):
        """Create a new order"""
        data = orders_namespace.payload

        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        new_order = Order(
            size=data["size"],
            flavour=data["flavour"],
            user_id=user.id
        )
        new_order.save()

        return new_order, HTTPStatus.CREATED
    

@orders_namespace.route('/<order_id>')
class ChangeOrder(Resource):
    """GET, UPDATE, DELETE an order with the id order_id"""
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description="Retrieve an order by an ID",
        params={
            "order_id": "The ID of the order to retrieve"
        }
    )
    @jwt_required()
    def get(self, order_id):
        """Retrieve an order by id"""
        order = Order.get_by_id(order_id)

        return order, HTTPStatus.OK

    @orders_namespace.expect(order_model)
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description="Update an order by ID",
        params={
            "order_id": "The ID of the order to update"
        }
    )
    @jwt_required()
    def put(self, order_id):
        """Update an order with id"""
        order_to_update = Order.get_by_id(order_id)
        if order_to_update:
            for key, val in orders_namespace.payload.items():
                setattr(order_to_update, key, val)

            order_to_update.commit()

            return order_to_update, HTTPStatus.OK
        else:
            return {"msg": "No Order Found!"}

    @jwt_required()
    @orders_namespace.doc(
        description="Delete an order with an ID",
        params={
            "order_id": "The ID of the order to delete"
        }
    )
    def delete(self, order_id):
        """Delete an order with id"""
        order = Order.get_by_id(order_id)
        if order:
            order.delete()
            
            return {"msg": "Order Deleted!"}, HTTPStatus.OK
        else:
            return {"msg": "Order not Found!"}, HTTPStatus.NOT_FOUND

@orders_namespace.route("/user/<user_id>/<order_id>")
class UserOrder(Resource):
    """Retrieve the user's order by id"""
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description="Retieve a user's order by ID",
        params={
                "order_id": "The ID of the order to retrieve",
                "user_id": "The ID of the user who made the order"
            }
    )
    @jwt_required()
    def get(self, user_id, order_id):
        """Retrieve the user's order by id"""
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id, user_id=user.id).first()

        return order, HTTPStatus.OK

@orders_namespace.route("/user/<user_id>/orders")
class UserOrders(Resource):
    """User orders"""
    @orders_namespace.marshal_list_with(order_model)
    @orders_namespace.doc(
        description="Retieve all the orders placed by a user",
        params={
                "user_id": "The user's ID"
            }
    )
    @jwt_required()
    def get(self, user_id):
        """Get all orders for a specific user with id"""
        user = User.get_by_id(user_id)
        orders = user.orders

        return orders, HTTPStatus.OK

@orders_namespace.route("/status/<order_id>")
class UpdateOrderStatus(Resource):
    """Update order status"""
    @orders_namespace.expect(order_status_model)
    @orders_namespace.marshal_with(order_status_model)
    @orders_namespace.doc(
        description="Update the order status",
        params={
            "order_id": "The ID of the order whose status should be updated"
        }
    )
    @jwt_required()
    def patch(self, order_id):
        """Update an order's status"""
        data = orders_namespace.payload
        order_to_update = Order.get_by_id(order_id)

        order_to_update.order_status = data["order_status"]
        order_to_update.commit()

        return order_to_update, HTTPStatus.OK