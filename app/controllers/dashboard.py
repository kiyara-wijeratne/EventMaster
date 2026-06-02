from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import login_required
from sqlalchemy import func

from app.models import db

from app.controllers.auth import role_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    return render_template('dashboard.html')