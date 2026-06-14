# adapted from
# https://flask.palletsprojects.com/en/stable/tutorial/views/

from functools import wraps

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_user

from app.models.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.get_by_email(email)

        if user and user.verify_password(password):
            # adapted from
            # https://flask-login.readthedocs.io/en/latest/#your-user-class
            login_user(user)
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid email or password. Please try again.", "error")

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# adapted from
# https://blog.stackademic.com/implementing-role-based-access-control-rbac-in-flask-f7e69db698f6
def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.role.name not in roles:
                return abort(403)  # Forbidden access
            return func(*args, **kwargs)

        return decorated_view

    return wrapper
