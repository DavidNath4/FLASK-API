from flask_restx import Namespace, Resource, fields
from flask import jsonify, request
from http import HTTPStatus

from ..utils import db
from ..models.models import User, Movie, User_Movie_List

from ..logs.logs import logger

from flask_jwt_extended import jwt_required, get_jwt_identity

management_ns = Namespace('management', 'Namespace for users')


@management_ns.route('/SelectMovie')
class SelectMovie(Resource):
    @management_ns.doc(description="Select a movie as a favorite for the user")
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            
            user_id = data.get('user_id'),
            movie_id = data.get('movie_id'),
            review = data.get('review'),
            
            select_movie = User_Movie_List(
                user_id = user_id,
                movie_id = movie_id,
                review = review            
            )
            
            db.session.add(select_movie)
            db.session.commit()                        
            
            return {
                "status" : HTTPStatus.OK,
                "message" : f"Select Movies to Favorite"            
            }, HTTPStatus.OK
            
        except Exception as e:
            logger.info(str(e))
            return {
                "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                "message" : str(e)            
            }, HTTPStatus.INTERNAL_SERVER_ERROR

@management_ns.route('/GetAllSelectedMovie/<int:user_id>')
class GetAllSelectedMovie(Resource):
    @management_ns.doc(description="Select a movie as a favorite for the user")
    @jwt_required()
    def get(self, user_id):
        try:
            movies = Movie.query.join(User_Movie_List).filter(User_Movie_List.user_id == user_id).all()
            data_movies_list = []
            
            for movie in movies:
                user_movie = User_Movie_List.query.filter_by(user_id=user_id, movie_id=movie.id).first()
                
                data_movies = {
                "id": movie.id,
                "title": movie.title,
                "genre": movie.genre,
                "review": user_movie.review ,
                "age_ratings" : movie.age_ratings.rating
            }
                data_movies_list.append(data_movies)            
            
            if len(data_movies_list) == 0:
                return {
                "status" : HTTPStatus.OK,
                "message" : f"No Movies Selected.",
                "data" : data_movies_list
            }, HTTPStatus.OK
            
            
            return {
                "status" : HTTPStatus.OK,
                "message" : f"Succes Retreived Movies.",
                "data" : data_movies_list
            }, HTTPStatus.OK
            
        except Exception as e:
            logger.info(str(e))
            return {
                "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                "message" : str(e)            
            }, HTTPStatus.INTERNAL_SERVER_ERROR

@management_ns.route('/RemoveSelectedMovie/<int:user_id>/<int:movie_id>')
class RemoveSelectedMovie(Resource):
    @management_ns.doc(description="Remove a movie from the user's list")
    @jwt_required()
    def delete(self, user_id, movie_id):
        try:
            user_movie = User_Movie_List.query.filter_by(user_id=user_id, movie_id=movie_id).first()
            
            if user_movie:                
                db.session.delete(user_movie)
                db.session.commit()
                
                return {
                    "status": HTTPStatus.OK,
                    "message": f"Movie removed from favorites",
                }, HTTPStatus.OK
            else:
                return {
                    "status": HTTPStatus.NOT_FOUND,
                    "message": "Movie not found in user's favorites",
                }, HTTPStatus.NOT_FOUND
        
        except Exception as e:
            logger.info(str(e))
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "message": str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR

@management_ns.route('/UpdateSelectedMovie/<int:user_id>/<int:movie_id>')
class UpdateSelectedMovie(Resource):
    @management_ns.doc(description="Remove a movie from the user's list")
    @jwt_required()
    def put(self, user_id, movie_id):
        try:
            data = request.get_json()
            user_movie = User_Movie_List.query.filter_by(user_id=user_id, movie_id=movie_id).first()
            
            if user_movie:                
                user_movie.review = data.get('review')
                db.session.commit()
                
                return {
                    "status": HTTPStatus.OK,
                    "message": f"Review Updated.",
                    "data" : {
                        "review" : user_movie.review
                    }
                }, HTTPStatus.OK
            else:
                return {
                    "status": HTTPStatus.NOT_FOUND,
                    "message": "Movie not found in user's favorites",
                }, HTTPStatus.NOT_FOUND
        
        except Exception as e:
            logger.info(str(e))
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "message": str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR




@management_ns.route('/GetAllMovieUser/<int:movie_id>')
class GetAllMovieUser(Resource):
    @management_ns.doc(description="Show users selected movie")
    def get(self, movie_id):
        try:
            users = User.query.join(User_Movie_List).filter(User_Movie_List.movie_id == movie_id).all()
            data_users_list = []
            
            for user in users:
                movie_user = User_Movie_List.query.filter_by(movie_id=movie_id, user_id=user.id).first()
                
                data_users = {
                "id": user.id,
                "name": user.name,                
                "review": movie_user.review ,                
            }
                data_users_list.append(data_users)            
            
            if len(data_users_list) == 0:
                return {
                "status" : HTTPStatus.OK,
                "message" : f"No Movies Selected.",
                "data" : data_users_list
            }, HTTPStatus.OK
            
            
            return {
                "status" : HTTPStatus.OK,
                "message" : f"Succes Retreived Movies.",
                "data" : data_users_list
            }, HTTPStatus.OK
            
        except Exception as e:
            logger.info(str(e))
            return {
                "status" : HTTPStatus.INTERNAL_SERVER_ERROR,
                "message" : str(e)            
            }, HTTPStatus.INTERNAL_SERVER_ERROR




        
        
