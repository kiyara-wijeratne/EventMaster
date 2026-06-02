import os

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.models import db
from app.models.user import User

from app.controllers.auth import bp
from app.controllers.dashboard import dashboard_bp
from app.controllers.events import events_bp
from app.controllers.registrations import registrations_bp
from app.controllers.speakers import speakers_bp
from app.controllers.reports import reports_bp
from app.controllers.settings import settings_bp

def create_app(config_filename='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    # bind database to app
    db.init_app(app)
    
    login_manager = LoginManager()
    # initalise login manager
    login_manager.init_app(app)
    # redirect users to login page
    login_manager.login_view = 'auth.login'
    
    # callback to load user object
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))
    
    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # create database tables
    with app.app_context():
        db.create_all()
    
    # register blueprints
    app.register_blueprint(bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(speakers_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    return app