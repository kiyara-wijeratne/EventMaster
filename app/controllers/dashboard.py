# adapted from
# https://flask.palletsprojects.com/en/stable/tutorial/views/

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from app.models.event import Event
from app.models.registration import Registration

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=("GET", "POST"))
@login_required
def index():
    # handle event delete
    if request.method == "POST":
        event_id = request.form.get("event_id")
        event = Event.get_by_id(event_id)

        if event:
            event.delete()
            flash("Event deleted successfully!", "success")
        else:
            flash("Event not found.", "error")

        return redirect(url_for("events.index"))

    # calculate total number of attendees
    approved_attendees = Registration.get_attendees("Approved")
    total_attendees = len(approved_attendees)

    # calculate ticket revenue from attendees
    revenue = sum(
        registration.ticket_type.price
        for registration in approved_attendees
        if registration.ticket_type
    )

    # get events
    all_events = Event.query.order_by(Event.event_start.asc()).all()

    return render_template(
        "dashboard.html",
        total_attendees=total_attendees,
        revenue=revenue,
        all_events=all_events,
    )
