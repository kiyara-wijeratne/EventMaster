from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime

from app.models import db

from app.models.event import Event
from app.models.event_type import EventType

from app.controllers.auth import role_required

events_bp = Blueprint('events', __name__, url_prefix="/events")

@events_bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    all_events = Event.query.all()
    
    return render_template('events.html', all_events=all_events, event=None, all_event_types=None)

@events_bp.route('/manage-event', methods=('GET', 'POST'))
@login_required
@role_required('Organiser')
def manage_event():
   all_event_types = EventType.query.all()
   
   # edit event clicked 
   # pre-fill event details
   event_id = request.args.get("event_id")
   event = Event.get_by_id(event_id) if event_id else None
   
   
   if request.method == 'POST':
       try:

           title = request.form['title']
           venue = request.form['venue']
           capacity = int(request.form['capacity'])
           event_start = datetime.fromisoformat(request.form['event_start'])
           event_end = datetime.fromisoformat(request.form['event_end'])
           
        # update existing event
           if event:
               
               # only the event organiser can edit the event
               if event.organiser_id != current_user.id:
                   abort(403)
                   
                   
               event.update(title=title, venue=venue, capacity=capacity)
               event.reschedule(event_start, event_end)
               
               flash('Event updated successfully!', 'success')
               return redirect(url_for('events.index'))
           
           else:
               # create new event
               
               event_type_id = request.form['event_type_id']
               
               Event.create(title=title,
                            event_type_id=event_type_id,
                            venue=venue,
                            capacity=capacity,
                            event_start=event_start,
                            event_end=event_end,
                            organiser_id=current_user.id)
               

               flash('Event created successfully!', 'success')
               return redirect(url_for('events.index'))
           
       except Exception as error:
           flash(str(error), 'error')
           return redirect(url_for('events.manage_event', event_id=event_id if event else None))
       
   return render_template('events.html', event=event, all_event_types=all_event_types)