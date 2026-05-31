import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models import db

def create_app(config_filename='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    # bind database to app
    db.init_app(app)
    
    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def hello():
        return "EventMaster"
    
    return app