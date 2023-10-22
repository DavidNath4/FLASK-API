from http import HTTPStatus
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from ..utils import db
from ..models.models import User

auth_ns = Namespace('auth', description='Namespace for authentication')



@auth_ns.route('/Register')
class SignUp(Resource):
    @auth_ns.doc(description = "Create new user data")    
    def post(self):
        """Register new user data"""
        data = request.get_json()
        # bcrypt = current_app.extensions['bcrypt']

        new_user = User(
                name = data.get('name'),
                email = data.get('email'),
                phone = data.get('phone'),
                password = data.get('password')
                )

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.email)
        refresh_token = create_refresh_token(identity=new_user.email)

        return {'email': new_user.email, 'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.CREATED