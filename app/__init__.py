from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration from .env file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Register routes
    from app.routes import auth
    from app.admin import admin
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    
    return app