from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func
from app.models import db

speakers_bp = Blueprint('speakers', __name__)

@speakers_bp.route('/speakers')
def index():
    return render_template('speakers.html')