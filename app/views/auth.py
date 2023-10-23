from http import HTTPStatus
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt, get_jti

from ..utils import db
from ..models.models import User

from ..logs.logs import logger

auth_ns = Namespace('auth', description='Namespace for authentication')



@auth_ns.route('/Register')
class Register(Resource):
    @auth_ns.doc(description = "Register new user data")    
    def post(self):
        """Register new user data"""
        logger.debug("Debug Regsiter AUTH")
        try:
            data = request.get_json()
            bcrypt = current_app.extensions['bcrypt']

            new_user = User(
                    name = data.get('name'),
                    email = data.get('email'),
                    phone = data.get('phone'),
                    password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
                    )

            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=new_user.email)
            refresh_token = create_refresh_token(identity=new_user.email)
            
            return {
                "status" : HTTPStatus.CREATED,
                "message" : "Success Retrieved Data.",
                "data" : {
                    'id' : new_user.id,
                    'email' : new_user.email,
                    'phone' : new_user.phone,
                    'access_token' : access_token,
                    'refresh_token' : refresh_token
                    }
                }, HTTPStatus.CREATED
            
        except Exception as e:
            logger.info(str(e))
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_ns.route('/Login')
class Login(Resource):
    @auth_ns.doc(description = "Login to system")
    def post(self):
        """Login to system"""
        logger.debug("Debug LOGIN AUTH")
        try:
            data = request.get_json()
            bcrypt = current_app.extensions['bcrypt']

            user = User.query.filter_by(email=data.get('email')).first()
            
            if(not user):
                return {
                        "status" : HTTPStatus.NOT_FOUND,
                        "message" : 'Email is not found.',
                    }, HTTPStatus.NOT_FOUND

            checkPassword = bcrypt.check_password_hash(user.password, data.get('password'))
            print(checkPassword)
            logger.info(checkPassword)

            if(checkPassword is False):            
                return {
                        "status" : HTTPStatus.UNAUTHORIZED,
                        "message" : 'Password is incorrect.',
                    }, HTTPStatus.UNAUTHORIZED

            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            
            return {
                "status" : HTTPStatus.OK,
                "message" : "Success Login.",
                "data" : {
                    'id' : user.id,
                    'email' : user.email,
                    'access_token' : access_token,
                    'refresh_token' : refresh_token
                    }
                }, HTTPStatus.OK

        except Exception as e:
            logger.info(str(e))
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR



@auth_ns.route('/refresh')
class Refresh(Resource):
    @auth_ns.doc(params={'Authorization': {'in': 'header', 'description': 'Refresh Token'}})    
    @jwt_required(refresh=True)
    def post(self):
        """Get refreshed token"""
        logger.debug("Debug refresh AUTH")
        try:
            data = request.get_json()
            email = get_jwt_identity()

            access_token = create_access_token(identity=email, fresh=True)
            
            return {
                    "status" : HTTPStatus.CREATED,
                    "message" : "Success Refresh Token.",
                    "data" : {
                        'access_token' : access_token,
                        'refresh_token' : data.get('refresh_token')
                        }
                    }, HTTPStatus.CREATED
            
        except Exception as e :
            logger.info(str(e))
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

