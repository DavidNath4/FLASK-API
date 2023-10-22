from ..utils import db
from sqlalchemy import Enum


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    
    user_movie_list = db.relationship('User_Movie_List', backref = 'user')
    
    def __repr__(self):
        return f"<User: {self.name}>"


class User_Movie_List(db.Model):
    __tablename__ = "user_movie_list"
    id = db.Column(db.Integer, primary_key = True)
    
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer(), db.ForeignKey('movie.id'))
    
    review = db.Column(db.String(255), nullable = True)



class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)        
    genre = db.Column(db.String(50), nullable=False)
    
    user_movie_list = db.relationship('User_Movie_List', backref = 'movie')
        
    age_ratings_id = db.Column(db.Integer(), db.ForeignKey('age_ratings.id'), nullable = True)
    
    def __repr__(self):
        return f"<Movie: {self.title}>"


class Age_Ratings(db.Model):
    __tablename__ = "age_ratings"
    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.String(50), nullable = False)
        
    movie = db.relationship('Movie', backref = 'age_ratings')
    
    def __repr__(self):
        return f"<Age_Rating: {self.rating}"