from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from app.models import db
from app.models.registration import Registration
from app.models.event import Event
from app.models.check_in import CheckIn

from app.controllers.auth import role_required

registrations_bp = Blueprint('registrations', __name__, url_prefix='/registrations')

@registrations_bp.route('/attendee-list', methods=('GET',))
@login_required
def attendee_list():
    selected_event_id = request.args.get('event_id', type=int)
    
    # get events to populate dropdown
    all_events = Event.query.order_by(Event.event_start.desc()).all()
    approved_attendees = Registration.get_attendees("Approved", filter_event_id=selected_event_id)
    
    return render_template('registrations.html', 
                           all_events=all_events, 
                           approved_attendees=approved_attendees, 
                           event_id=selected_event_id)

@registrations_bp.route('/check-in-queue', methods=('GET', 'POST'))
@login_required
@role_required('Coordinator')
def check_in_queue():
    if request.method == 'POST':
        selected_event_id = request.form.get('event_id', type=int)
        
        registration_id = request.form.get('registration_id')
        registration = Registration.get_by_id(registration_id)
        
        if registration:
            # check attendee is not already checked in 
            if not registration.check_in:
                CheckIn.create(registration_id=registration_id,
                            coordinator_id=current_user.id)
                
                flash(f'Successfully checked in {registration.attendee.full_name}', 'success')
            else:
                flash(f'{registration.attendee.full_name} is already checked in', 'error')
        else:
            flash('Registration not found', 'error')
    
        # redirect so user can keep checking in, event filter active
        return redirect(url_for('registrations.check_in_queue', event_id=selected_event_id))
    
    selected_event_id = request.args.get('event_id', type=int)
    
    # get events to populate dropdown
    all_events = Event.query.order_by(Event.event_start.desc()).all()
    approved_attendees = Registration.get_attendees("Approved", filter_event_id=selected_event_id)
    
    return render_template('registrations.html', 
                           all_events=all_events, 
                           approved_attendees=approved_attendees, 
                           event_id=selected_event_id)

@registrations_bp.route('/pending-approval', methods=('GET', 'POST'))
@login_required
@role_required('Coordinator')
def pending_approval():
    if request.method == 'POST':
        selected_event_id = request.form.get('event_id', type=int)
        
        registration_id = request.form.get('registration_id')
        registration = Registration.get_by_id(registration_id)
        
        if registration:
            try:
                registration.approve()
                flash(f'Successfully approved {registration.attendee.full_name}', 'success')
            except Exception as error:
                flash(str(error), 'error')
                
            # redirect so user can keep approving, event filter active
            return redirect(url_for('registrations.pending_approval', event_id=selected_event_id))
    
    selected_event_id = request.args.get('event_id', type=int)
    
    # get events to populate dropdown
    all_events = Event.query.order_by(Event.event_start.desc()).all()
    waitlisted_attendees = Registration.get_attendees("Waitlisted", filter_event_id=selected_event_id)
    
    return render_template('registrations.html', 
                           all_events=all_events, 
                           waitlisted_attendees=waitlisted_attendees, 
                           event_id=selected_event_id)