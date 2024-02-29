from flask_restx import Namespace, Resource, fields
from ..models.review import Review
from ..models.user import User
from ..models.restaurant import Restaurant
from http import HTTPStatus
from flask_cors import cross_origin
from flask import jsonify


review_namespace = Namespace("Review Namespace", description="review endpoints")

review_model = review_namespace.model(
    "Review", {
        "id": fields.String(),
        "first_name": fields.String(),
        "last_name": fields.String(),
        "text": fields.String(),
        "rating": fields.Integer(),
        "restaurant_id": fields.String(),
        "user_id": fields.String()
    }
)

@review_namespace.route("/create-review")
class CreateReviews(Resource):
    """Create reviews"""
    @review_namespace.expect(review_model)
    @review_namespace.marshal_with(review_model)
    def post(self):
        """Create a review"""
        data = review_namespace.payload

        user = User.query.filter_by(email=data["user_id"]).first()
        restaurant = Restaurant.query.filter_by(name=data["restaurant_id"]).first()
        new_review = Review(
            first_name=data["first_name"],
            last_name=data["last_name"],
            text=data["text"],
            rating=data["rating"],
            user_id=user.id,
            restaurant_id=restaurant.id,
        )

        new_review.save()

        return new_review, HTTPStatus.CREATED


@review_namespace.route("/restaurant/<restaurant_slug>")
class RestaurantReviews(Resource):
    """Retrieve a restaurant reviews"""
    @cross_origin(origin='localhost')
    @review_namespace.marshal_list_with(review_model)
    def get(self, restaurant_slug):
        """Get restaurant reviews"""
        restaurant = Restaurant.query.filter_by(slug=restaurant_slug).first()
        if not restaurant:
            return [], HTTPStatus.OK

        reviews = restaurant.reviews
        return reviews, HTTPStatus.OK
