from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func
from app.models import db

events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def index():
    return render_template('events.html')