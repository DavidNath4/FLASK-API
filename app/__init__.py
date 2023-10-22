from flask import Flask
from flask_restx import Api
from .config.config import config_dict
from .views.user import user_ns
from .views.movie import movie_ns
from .views.age_rating import age_rating_ns
from .views.user_movie_management import management_ns
from .views.auth import auth_ns
from .utils import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import models
from .logs.logs import logger
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

def create_app(config = config_dict['dev']):
    
    logger.debug("initial debug")
    
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    
    api = Api(
        app,
        doc='/docs',
        title="Rest API Flask",
        description="Simple API project with Flask"
    )
    
    
    api.add_namespace(user_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(age_rating_ns)
    api.add_namespace(management_ns)
    api.add_namespace(auth_ns)
    
    migrate = Migrate(app, db)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    
    
    return app