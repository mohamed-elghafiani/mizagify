from flask_restx import Namespace, Resource, fields, marshal
from flask import request, jsonify, make_response, Response
import json
from ..models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict, BadRequest
from flask_cors import cross_origin


auth_namespace = Namespace("auth", description="A Namespace for auth Blueprint")
signup_model = auth_namespace.model(
    'SignUp', {
        'id': fields.String(),
        'username': fields.String(required=True, description='A username'),
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='An password'),
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.String(),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'email': fields.String(required=True, description='An email'),
        'phone': fields.String(required=True, description='An email'),
        'password_hash': fields.String(required=True, description='A password'),
        'city': fields.String(description="Location"),
    }
)

auth_response = auth_namespace.model("Response", {
    "msg": fields.String()
})

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password'),
    }
)

login_response = auth_namespace.model(
    'LoginResponse', {
        'access_token': fields.String(required=True, description='An email'),
        'refresh_token': fields.String(required=True, description='A password'),
    }
)

@auth_namespace.route('/signup')
class Signup(Resource):
    """Signup class"""
    @auth_namespace.expect(user_model)
    @auth_namespace.marshal_with(auth_response)
    def post(self):
        """Create a new user"""

        data = request.get_json()
        
        if User.query.filter_by(email=data.get("email")).first():
            return {"msg": "Email already exist. Try to login instead"}, HTTPStatus.OK

        new_user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password_hash=generate_password_hash(data.get("password")),
            phone=data.get("phone"),
            city=data.get("city")
        )
        new_user.save()
        
        return {"msg": "Accound created!"}, HTTPStatus.CREATED

@auth_namespace.route('/login')
class Login(Resource):
    """Login class"""
    @auth_namespace.expect(login_model)
    # @auth_namespace.marshal_with(login_response)
    def post(self):
        """Login a user"""
        data = request.get_json()
        
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user is not None and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            response_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "city": user.city,
                "phone": user.phone,
            }

            response = Response(json.dumps(response_data), status=200, mimetype='application/json')
            response.set_cookie("access_token", access_token, samesite="None", secure="False")

            return response

        raise BadRequest("Invalid usename or password!")
    
@auth_namespace.route("/refresh")
class Refresh(Resource):
    """Refresh JWT token"""
    @jwt_required(refresh=True)
    def post(self):
        """Refresh JWT token"""
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)

        return {
            "access_token": access_token
        }, HTTPStatus.OK


@auth_namespace.route("/me")
class Me(Resource):
    """A Me endpoint"""
    @jwt_required()
    @auth_namespace.marshal_with(user_model)
    def get(self):
        """Retrieve user data"""
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"msg": "Unauthorized request"}, HTTPStatus.UNAUTHORIZED

        return user, HTTPStatus.OK