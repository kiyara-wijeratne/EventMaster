# adapted from
# https://flask.palletsprojects.com/en/stable/tutorial/views/

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.controllers.auth import role_required
from app.models.role import Role
from app.models.user import User

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/account")
@login_required
def account():
    return render_template("settings.html")


@settings_bp.route("/permissions", methods=("GET", "POST"))
@login_required
@role_required("Administrator")
def permissions():
    if request.method == "POST":
        user_id = request.form["user_id"]
        role_id = request.form["role_id"]

        user = User.get_by_id(user_id)

        if user:
            user.assign_role(role_id)
            flash(f"Updated {user.full_name}'s role successfully", "success")
        else:
            flash("User or role could not be verified. Please try again.", "error")

        return redirect(url_for("settings.permissions"))

    # get all users and all roles to populate the dropdown
    all_users = User.query.all()
    all_roles = Role.query.all()

    return render_template("settings.html", all_users=all_users, all_roles=all_roles)
