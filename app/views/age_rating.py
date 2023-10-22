from flask_restx import Namespace, Resource, fields
from flask import jsonify, request
from http import HTTPStatus

from ..utils import db
from ..models.models import Age_Ratings

from ..logs.logs import logger

age_rating_ns = Namespace('age_rating', 'Namespace for Age Ratings')


age_rating_model = age_rating_ns.model(    
    'Age_Ratings', {                
        'rating': fields.String(description="user email field")
    }
)




@age_rating_ns.route('/Create')
class AgeRatingCreate(Resource):
    @age_rating_ns.doc(description = "Create User")    
    def post(self):
        logger.debug("Create age rating Logger")
        try:
            data = request.get_json()
            
            if data.get("rating") != None:
                new_rating = Age_Ratings(
                    rating = data.get('rating')
                    )
                
                db.session.add(new_rating)
                db.session.commit()
                
                return {
                "status" : HTTPStatus.CREATED,
                "message" : "Data Created.",
                "data" : {
                    "id": new_rating.id,
                    "rating" : new_rating.rating
                    }
                }, HTTPStatus.CREATED
                
            return {
                "status" : HTTPStatus.BAD_REQUEST,
                "message" : "Rating cant Empty."            
                }, HTTPStatus.BAD_REQUEST
        
        except Exception as e :            
            logger.info(str(e))
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR


@age_rating_ns.route('/')
class AgeRatingAll(Resource):
    @age_rating_ns.doc(description = "Get all age rating data")        
    def get(self):
        logger.debug("Get age rating Logger")
        try:
            age_ratings = Age_Ratings.query.all()
            age_rating_list = []
            
            for i in age_ratings:
                data_to_list = {
                    "id" : i.id,
                    "rating" : i.rating                    
                }
                age_rating_list.append(data_to_list)
            
            if age_ratings:                
                return {
                    "status" : HTTPStatus.OK,
                    "message" : "Success Retrieved Data.",
                    "data" : age_rating_list
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


@age_rating_ns.route('/<int:id>')
class AgeRatingGetById(Resource):
    @age_rating_ns.doc(description = "Get User by ID",
                       params = 
                           {"id":"id parameter"}
                       )        
    def get(self, id):
        logger.debug("Get by ID age rating Logger")
        try:
            data = Age_Ratings.query.get(id)
            
            if data == None :
                return {
                    "status" : HTTPStatus.OK,
                    "message" : "No Data Found.",                    
                }, HTTPStatus.OK
                
            return {
                    "status" : HTTPStatus.OK,
                    "message" : "Success Retrieved Data.",
                    "data" : {
                        "id" : data.id,
                        "rating" : data.rating
                    }
                }, HTTPStatus.OK
        
        except Exception as e :
            logger.info(str(e))            
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR


@age_rating_ns.route('/Update/<int:id>')
class AgeRatingUpdate(Resource):
    @age_rating_ns.doc(description = "Update User by ID", 
                 params = {"id":"id parameter"})        
    def put(self, id):
        logger.debug("Update age rating Logger")
        try:
            data = request.get_json()
            data_to_update = Age_Ratings.query.get_or_404(id)                        
            
            data_to_update.rating = data["rating"]
            db.session.commit()
            
            return {
                "status" : HTTPStatus.OK,
                "message" : "Data Updated.",
                "data" : {
                    "id" : data_to_update.id,
                    "rating" : data_to_update.rating,                    
                    }
                }, HTTPStatus.OK

        except Exception as e :
            logger.info(str(e))            
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR
        

@age_rating_ns.route('/Remove/<int:id>')
class AgeRatingDelete(Resource):
    @age_rating_ns.doc(description = "Remove User by ID", 
                 params = {"id":"id parameter"})    
    def delete(self, id):
        logger.debug("Remove age rating Logger")            
        try:
            data_to_delete = Age_Ratings.query.get_or_404(id)
            
            db.session.delete(data_to_delete)
            db.session.commit()
            
            return {
                "status" : HTTPStatus.OK,
                "message" : "Data Successfully Remove.",
            }, HTTPStatus.OK        

        except Exception as e :
            logger.info(str(e))            
            return {
                    "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message" : str(e),                    
                }, HTTPStatus.INTERNAL_SERVER_ERROR