import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.get_by_email(email)
        
        if user and user.verify_password(password):
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            
    return render_template('auth/login.html')