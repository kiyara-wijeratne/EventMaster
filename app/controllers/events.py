from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime

from app.models import db

from app.models.event import Event
from app.models.event_type import EventType
from app.models.event_branding import EventBranding
from app.models.ticket_type import TicketType
from app.models.session import Session
from app.models.speaker import Speaker
from app.models.presentation_material import PresentationMaterial

from app.controllers.auth import role_required

events_bp = Blueprint('events', __name__, url_prefix="/events")

@events_bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        event = Event.get_by_id(event_id)
        
        if event:
            event.delete()
            flash('Event deleted successfully!', 'success')
        else:
            flash('Event not found.', 'error')
        
        return redirect(url_for('events.index'))
    
    all_events = Event.query.all() 
    return render_template('events.html', all_events=all_events)

@events_bp.route('/manage-event', methods=('GET', 'POST'))
@login_required
@role_required('Organiser')
def manage_event():
        
    # get event details
    event_id = request.args.get('event_id')
    event = Event.get_by_id(event_id) if event_id else None
    event_branding = EventBranding.get_by_event_id(event.id) if event else None
    
    # get event types to populate dropdown
    all_event_types = EventType.query.all()
    # get speakers to populate dropdown
    all_speakers = Speaker.query.all()
    
    if request.method == 'POST':
        try:
            
            # indentify what the user is trying to do
            action = request.form.get('action')
            
            if action == "save_event":
                event = save_event(event)
                
                flash('Event saved successfully!', 'success')
                return redirect(url_for('events.index'))
                
            elif action == "create_branding":
                create_branding(event)
                flash('Branding created successfully!', 'success')
                
            elif action == "update_branding":
                update_branding(event)
                flash('Branding saved successfully!', 'success')
                
            elif action == "delete_branding":
                delete_branding(event)
                flash('Branding deleted successfully!', 'success')
                
            elif action == "create_ticket":
                create_ticket(event)
                flash('Ticket created successfully!', 'success')
                
            elif action == "update_ticket":
                update_ticket()
                flash('Ticket saved successfully!', 'success')
                
            elif action == "delete_ticket":
                delete_ticket()
                flash('Ticket deleted successfully!', 'success')
                
            elif action == "create_session":
                create_session(event)
                flash('Session created successfully!', 'success')
                
            elif action == "update_session":
                update_session()
                flash('Session saved successfully!', 'success')
                
            elif action == "delete_session":
                delete_session()
                flash('Session deleted successfully!', 'success')
                
            if event:
                # redirect so user can continue editing
                return redirect(url_for('events.manage_event', event_id=event.id))
            else:
                return redirect(url_for('events.index'))
                
        except Exception as error:
            flash(str(error), 'error')
            return redirect(url_for('events.manage_event', event_id=event.id if event else None))
    
    return render_template('events.html',
                           event=event,
                           event_branding=event_branding,
                           all_event_types=all_event_types,
                           all_speakers=all_speakers)
    
def save_event(event):
    
    # get core logistical details
    title = request.form['title']
    venue = request.form['venue']
    capacity = int(request.form['capacity'])
    event_start = datetime.fromisoformat(request.form['event_start'])
    event_end = datetime.fromisoformat(request.form['event_end'])
    
    # create new event
    if not event:
        event_type_id = request.form['event_type_id']
        
        return Event.create(title=title,
                             event_type_id=event_type_id,
                             venue=venue,
                             capacity=capacity,
                             event_start=event_start,
                             event_end=event_end,
                             organiser_id=current_user.id)
        
    # update existing event
    # only the event organiser can edit the event
    if event.organiser_id != current_user.id:
        abort(403)
            
    event.update(title=title, venue=venue, capacity=capacity)
    event.reschedule(event_start, event_end)
        
    return event

def create_branding(event):
    EventBranding.create(event_id=event.id,
                         logo_path=request.form['logo_path'],
                         primary_colour=request.form['primary_colour'],
                         secondary_colour=request.form['secondary_colour'])
        
def update_branding(event):
    branding = EventBranding.get_by_event_id(event.id)
    
    if branding:
        branding.update(logo_path=request.form['logo_path'],
                        primary_colour=request.form['primary_colour'],
                        secondary_colour=request.form['secondary_colour'])
    
def delete_branding(event):
    branding = EventBranding.get_by_event_id(event.id)
    
    if branding:
        branding.delete()
    
def create_ticket(event):
    TicketType.create(event_id=event.id,
                      name=request.form['name'],
                      max_quantity=int(request.form['max_quantity']),
                      sales_start=datetime.fromisoformat(request.form['sales_start']),
                      sales_end=datetime.fromisoformat(request.form['sales_end']),
                      price=int(request.form['price']))
    
def update_ticket():
    ticket = TicketType.get_by_id(request.form['ticket_id'])
    
    if ticket:   
        ticket.update(name=request.form['name'],
                    max_quantity=int(request.form['max_quantity']),
                    sales_start=datetime.fromisoformat(request.form['sales_start']),
                    sales_end=datetime.fromisoformat(request.form['sales_end']),
                    price=int(request.form['price']))
    
def delete_ticket():
    ticket = TicketType.get_by_id(request.form['ticket_id'])
    
    if ticket:
        ticket.delete()
    
        
def create_session(event):
    session = Session.create(event_id=event.id,
                             title=request.form['title'],
                             session_start=datetime.fromisoformat(request.form['session_start']),
                             session_end=datetime.fromisoformat(request.form['session_end']),
                             room=request.form['room'])
    
    speaker_id = request.form.get('speaker_id')
    if speaker_id:
        session.add_speaker(int(speaker_id))
        
        # if speaker assigned, presentation materials can be assigned
        file_path = request.form.get('file_path')
        if file_path:
            PresentationMaterial.create(speaker_id=speaker_id,
                                        session_id=session.id,
                                        file_path=file_path)
         
def update_session():
    session = Session.get_by_id(request.form['session_id'])
    
    if session:
    
        session.update(title=request.form['title'],
                    room=request.form['room'])
        
        session.reschedule(datetime.fromisoformat(request.form['session_start']), 
                        datetime.fromisoformat(request.form['session_end']))
        
        new_speaker = request.form.get('speaker_id')
        new_speaker_id = int(new_speaker) if new_speaker else None
        
        if new_speaker_id:
            # check if speaker was changed
            current_speaker_id = session.speakers[0].id if session.speakers else None
            
            # speaker changed
            speaker_changed = new_speaker_id != current_speaker_id
            if  speaker_changed:
                # remove old speaker
                # removed linked presentation mateiral too
                if current_speaker_id:
                    session.remove_speaker(current_speaker_id)
                
                # add new speaker
                if new_speaker_id:
                    session.add_speaker(new_speaker_id)
               
                    
            # if speaker assigned, presentation materials can be managed 
            file_path = request.form.get('file_path')

            # check if presentation materials already exist
            existing_materials = PresentationMaterial.get_by_session_id(session.id)
            existing_material = existing_materials[0] if existing_materials else None

            if file_path:
                # if they provided a path, and the speaker didn't change, UPDATE
                if existing_material and not speaker_changed:
                    existing_material.update(file_path=file_path)
                else:
                    # else (new speaker or no previous material), CREATE
                    PresentationMaterial.create(speaker_id=new_speaker_id,
                                                session_id=session.id,
                                                file_path=file_path)
            else:
                # if file_path text box blank, DELETE
                if existing_material:
                    existing_material.delete()
    
def delete_session():
    session = Session.get_by_id(request.form['session_id'])
    
    if session:
        session.delete()