from functools import wraps 
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_user
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.get_by_email(email)
        
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            
    return render_template('auth/login.html')

def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.role.name not in roles:
                return abort(403)  # Forbidden access
            return func(*args, **kwargs)
        return decorated_view
    return wrapper