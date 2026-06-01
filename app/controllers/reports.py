from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func
from app.models import db

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
def index():
    return render_template('reports.html')