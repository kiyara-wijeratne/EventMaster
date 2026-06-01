import os

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from app.models import db

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
    
    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # create database tables
    with app.app_context():
        db.create_all()
    
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