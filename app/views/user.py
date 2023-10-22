from flask_restx import Namespace, Resource, fields
from flask import jsonify, request
from http import HTTPStatus

from ..utils import db
from ..models.models import User

from ..logs.logs import logger

user_ns = Namespace('user', 'Namespace for users')


user_model = user_ns.model(    
    'User', {        
        'name': fields.String(required=True, description="user name field"),
        'email': fields.String(required=True, description="user email field"),
        'phone': fields.String(required=True, description="user phone field"),
        'password': fields.String(required=True, description="user password field"),
    }
)

user_get_model = user_ns.model(
    'User', {
        "id" : fields.String(required=True, description="user id field"),
        'name': fields.String(required=True, description="user name field"),
        'email': fields.String(required=True, description="user email field"),
        'phone': fields.String(required=True, description="user phone field"),
        'password': fields.String(required=True, description="user password field"),
    }
)

user_response_get_model = user_ns.model(
    'Response', {
        'status' : fields.Integer(required=True, description="HTTP Status Code"),
        'message' : fields.String(required=True, description="Message status"),
        'data' : fields.Nested(user_get_model)
    }
)

# CREATE
@user_ns.route('/Create')
class UserRegister(Resource):
    @user_ns.doc(description = "Create User")    
    def post(self):
        logger.debug("Create age rating Logger")
        try:
            data = request.get_json()            
            
            new_user = User(
                name = data.get('name'),
                email = data.get('email'),
                phone = data.get('phone'),
                password = data.get('password')
                )
            
            if (new_user.name or new_user.email or new_user.phone or new_user.password) == None:                
                return {
                    "status" : HTTPStatus.BAD_REQUEST,
                    "message" : "Data Can't be Empty."                    
                    }, HTTPStatus.BAD_REQUEST

            db.session.add(new_user)
            db.session.commit()
            
            return {
                "status" : HTTPStatus.CREATED,
                "message" : "Data Created.",
                "data" : {
                    "id": new_user.id,
                    "name" : new_user.name,
                    "email" : new_user.email,
                    "phone" : new_user.phone
                }
                }, HTTPStatus.CREATED
        
        except Exception as e :
            logger.info(str(e))            
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR

# GET ALL
@user_ns.route('/')
class UserGetAll(Resource):
    @user_ns.doc(description = "Get all User")        
    def get(self):
        logger.debug("Get User Logger")
        try:
            users = User.query.all()
            user_list = []
            
            for i in users:
                data_to_list = {
                    "id" : i.id,
                    "title" : i.name,
                    "genre" : i.email,
                    "phone" : i.phone
                }
                user_list.append(data_to_list)
            
            if users:                
                return {
                    "status" : HTTPStatus.OK,
                    "message" : "Success Retrieved Data.",
                    "data" : user_list
                }, HTTPStatus.OK
                        
            
            return {
                    "status" : HTTPStatus.OK,
                    "message" : "No Data Found.",
                    "data" : []
                }, HTTPStatus.OK
            
        except Exception as e :
            logger.info(str(e))            
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR

# GET BY ID
@user_ns.route('/<int:user_id>')
class UserGetById(Resource):
    @user_ns.doc(description = "Get User by ID", 
                 params = {"user_id":"id parameter"})  
    def get(self, user_id):
        logger.debug("Get by ID User Logger")
        try:
            data = User.query.get(user_id)            
            
            if data == None :                
                return {
                    "status" : HTTPStatus.OK,
                    "message" : "No Data Found.",
                    "data" : []
                }, HTTPStatus.OK         
                        
            return {
                    "status" : HTTPStatus.OK,
                    "message" : "Success Retrieved Data.",
                    "data" : {
                        "id" : data.id,
                        "name" : data.name,
                        "email" : data.email,
                        "phone" : data.phone
                        }
                }, HTTPStatus.OK
        
        except Exception as e :            
            logger.info(str(e))            
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR
            
# UPDATE
@user_ns.route('/Update/<int:user_id>')
class UserUpdate(Resource):
    @user_ns.doc(description = "Get User by ID", 
                 params = {"user_id":"id parameter"})
    def put(self, user_id):        
        logger.debug("Update User Logger")
        try:            
            data = request.get_json()
            data_to_update = User.query.get_or_404(user_id)
            
            data_to_update.name = data["name"]
            data_to_update.email = data["email"]
            data_to_update.phone = data["phone"]
            data_to_update.password = data["password"]
            
            db.session.commit()
            
            return {
                "status" : HTTPStatus.OK,
                "message" : "Data Updated.",
                "data" : {
                    "id" : data_to_update.id,
                    "name" : data_to_update.name,
                    "email" : data_to_update.email,
                    "phone" : data_to_update.phone
                    }
                }, HTTPStatus.OK
        
        except Exception as e :
            logger.info(str(e))            
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR

# DELETE
@user_ns.route('/Remove/<int:user_id>')
class UserDelete(Resource):
    @user_ns.doc(description = "Get User by ID", 
                 params = {"user_id":"id parameter"})        
    def delete(self, user_id):        
        logger.debug("Remove User Logger")
        try:
            data_to_delete = User.query.get_or_404(user_id)
            
            db.session.delete(data_to_delete)
            db.session.commit()
            
            return {
                    "status" : HTTPStatus.OK,
                    "message" : "Success Remove Data",                    
                }, HTTPStatus.OK
        
        except Exception as e :            
            logger.info(str(e))
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR

