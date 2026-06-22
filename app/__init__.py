from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-this'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///securefin.db'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-change-this-make-it-longer-2024!'    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Register routes
    from app.routes import auth
    app.register_blueprint(auth)
    
    return app