from flask_restx import Namespace, Resource, fields
from flask import jsonify, request
from http import HTTPStatus

from ..utils import db
from ..models.models import Movie

from ..logs.logs import logger

movie_ns = Namespace('movie', 'Namespace for movies')

movie_model = movie_ns.model(
    'Movie',{        
        'title': fields.String(required=True, description="Movie title field"),        
        'genre': fields.String(required=True, description="Movie genre field"),
        'age_rating_id': fields.Integer(required=False, description="Age rating ID"),
    }
)


# CREATE
@movie_ns.route('/Create')
class MovieCreate(Resource):
    @movie_ns.doc(description="Create Movie")
    def post(self):
        logger.debug("Create Movie Logger")
        try:
            data = request.get_json()
            
            new_movie = Movie(
                title=data.get('title'),
                genre=data.get('genre'),
                age_ratings_id=data.get('age_ratings_id')
            )
            
            db.session.add(new_movie)
            db.session.commit()                        
            
            return {
                "status": HTTPStatus.CREATED,
                "message": "Data Created.",
                "data": {
                    "id" : new_movie.id,
                    "title": new_movie.title,
                    "genre": new_movie.genre,
                    "age_ratings_id": new_movie.age_ratings_id,                
            }
            }, HTTPStatus.CREATED
        
        except Exception as e:
            logger.error(str(e))
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, HTTPStatus.INTERNAL_SERVER_ERROR


# GET ALL DATA
@movie_ns.route('/')
class MovieGetAll(Resource):
    @movie_ns.doc(description="Get Movie All")
    def get(self):
        logger.debug("Get Movie Logger")
        try:            
            data = Movie.query.all()            
            data_list = []
            
            for i in data:                
                data_to_list = {
                    "id" : i.id,
                    "title" : i.title,
                    "genre" : i.genre,
                    "age_ratings_id" : i.age_ratings_id
                }
                data_list.append(data_to_list)                                         
            
            return {
                "status": HTTPStatus.OK,
                "message" : "Success Retrieved Data.",
                "data": data_list
            }, HTTPStatus.OK
        
        
        except Exception as e:
            logger.error(str(e))
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, HTTPStatus.INTERNAL_SERVER_ERROR

# GET BY ID
@movie_ns.route('/<int:id>')
class MovieGetByID(Resource):
    @movie_ns.doc(description="Get Movie By ID")
    def get(self, id):
        logger.debug("Get Movie Logger")
        try:
            data = Movie.query.get(id)
            
            return {
                "status": HTTPStatus.OK,
                "message" : "Success Retrieved Data.",
                "data": {
                    "id" : data.id,
                    "title" : data.title,
                    "genre" : data.genre,
                    "age_ratings_id" : data.age_ratings_id
                }
            }, HTTPStatus.OK
        
        
        except Exception as e:
            logger.error(str(e))
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, HTTPStatus.INTERNAL_SERVER_ERROR

# UPDATE
@movie_ns.route('/Update/<int:id>')
class MovieUpdate(Resource):
    @movie_ns.doc(description="Update Movie")
    def put(self, id):
        logger.debug("Update Movie Logger")
        try:
            data = request.get_json()            
            data_to_update = Movie.query.get(id)
                        
            data_to_update.title = data["title"]
            data_to_update.genre = data["genre"]
            data_to_update.age_ratings_id = data["age_ratings_id"]
                        
            db.session.commit()

            return {
                "status": HTTPStatus.OK,
                "message" : "Success Update Data.",
                "data": {
                    "id" : data_to_update.id,
                    "title" : data_to_update.title,
                    "genre" : data_to_update.genre,
                    "age_ratings_id" : data_to_update.age_ratings_id
                }
            }, HTTPStatus.OK
        
        
        except Exception as e:
            logger.error(str(e))
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "message": str(e),
                "data": []
            }, HTTPStatus.INTERNAL_SERVER_ERROR

# REMOVE
@movie_ns.route('/Remove/<int:id>')
class MovieRemove(Resource):
    @movie_ns.doc(description="Remove Movie")
    def delete(self, id):
        logger.debug("Remove Movie Logger")
        try:
            data = Movie.query.get_or_404(id)
            
            db.session.delete(data)
            db.session.commit()
            
            return {
                "status": HTTPStatus.OK,
                "message" : "Success Remove Data."                
            }, HTTPStatus.OK
        
        
        except Exception as e:
            logger.error(str(e))
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "message": str(e),                
            }, HTTPStatus.INTERNAL_SERVER_ERROR            