from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import login_required
from sqlalchemy import func

from app.models import db
from app.models.event import Event
from app.models.registration import Registration

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
@login_required
def index():
    selected_event_id = request.args.get('event_id', type=int)
    
    # get events to populate dropdown
    all_events = Event.query.order_by(Event.event_start.desc()).all()
    
    event = None
    total_attendees = 0
    ticket_labels = []
    ticket_values = []
    
    if selected_event_id:
        event = Event.get_by_id(selected_event_id)
        if event:
            
            # calculate total number of attendees
            approved_attendees = Registration.get_attendees("Approved", filter_event_id=event.id)
            total_attendees = len(approved_attendees)
            
            # group tickets by type for pie chart
            ticket_counts = {}
            for attendee in approved_attendees:
                ticket_name = attendee.ticket_type.name
                if ticket_name in ticket_counts:
                    ticket_counts[ticket_name] += 1
                else:
                    ticket_counts[ticket_name] = 1
                    
            # split dictionary into two lists for pie chart
            ticket_labels = list(ticket_counts.keys())
            ticket_values = list(ticket_counts.values())
        
 
    return render_template('reports.html',
                           all_events=all_events,
                           selected_event_id=selected_event_id,
                           event=event,
                           total_attendees=total_attendees,
                           ticket_labels=ticket_labels,
                           ticket_values=ticket_values)