from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func
from app.models import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def index():
    return render_template('dashboard.html')