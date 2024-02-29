from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


auth_namespace = Namespace("auth", description="A Namespace for auth Blueprint")
signup_model = auth_namespace.model(
    'SignUp', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='An password'),
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email': fields.String(required=True, description='An email'),
        'password_hash': fields.String(required=True, description='An password'),
        'is_active': fields.Boolean(description="This shows that the user if active"),
        'is_staff': fields.Boolean(description="This shows if user is staff")
    }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password'),
    }
)

@auth_namespace.route('/signup')
class Signup(Resource):
    """Signup class"""
    @auth_namespace.expect(user_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """Create a new user"""

        data = request.get_json()
        
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password_hash=generate_password_hash(data.get("password")),
        )
        new_user.save()

        return new_user, HTTPStatus.CREATED

@auth_namespace.route('/login')
class Login(Resource):
    """Login class"""
    @auth_namespace.expect(login_model)
    def post(self):
        """Login a user"""
        data = request.get_json()
        
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user is not None and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                "access_token": access_token,
                "refresh_toke": refresh_token
            }
            return response, HTTPStatus.OK
    
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