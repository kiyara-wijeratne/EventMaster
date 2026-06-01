from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func
from app.models import db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings')
def index():
    return render_template('settings.html')