from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func
from app.models import db

registrations_bp = Blueprint('registrations', __name__)

@registrations_bp.route('/registrations')
def index():
    return render_template('registrations.html')