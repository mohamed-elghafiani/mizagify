from flask_restx import Api
from .endpoints.user_endpoints import auth_namespace
from .endpoints.order_endpoints import orders_namespace
from .endpoints.availability_endpoints import avail_namespace
from .endpoints.restaurant_endpoints import restaurant_namepace
from .endpoints.review_endpoints import review_namespace
from .endpoints.reservation_endpoints import reservation_ns
from werkzeug.exceptions import NotFound, MethodNotAllowed


authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
    }
}

api = Api(
    title="TabaQ API",
    description="This is the BACKEND API of the TABAQ project",
    authorizations=authorizations,
    security="Bearer Auth"
)

api.add_namespace(auth_namespace, path="/api/auth")
api.add_namespace(orders_namespace, path="/api/orders")
api.add_namespace(avail_namespace, path="/api/avail")
api.add_namespace(restaurant_namepace, "/api/restaurants")
api.add_namespace(review_namespace, "/api/reviews")
api.add_namespace(reservation_ns, "/api/restaurant")


# Error Handlers
@api.errorhandler(NotFound)
def not_found(error):
    """Not Found Error Handler"""
    return {"error": "Not Found!"}, 404

@api.errorhandler(MethodNotAllowed)
def method_not_allowed(error):
    """Not Found Error Handler"""
    return {"error": "Method Not Allowed!"}, 405