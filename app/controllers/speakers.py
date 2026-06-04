from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func
from flask_login import login_required, current_user

from app.models import db
from app.models.speaker import Speaker

from app.controllers.auth import role_required

speakers_bp = Blueprint('speakers', __name__, url_prefix='/speakers')

@speakers_bp.route('/', methods=('GET',))
@login_required
def index():
    all_speakers = Speaker.query.all() 
    return render_template('speakers.html', all_speakers=all_speakers)

@speakers_bp.route('/manage-speaker', methods=('GET', 'POST'))
@login_required
@role_required('Organiser')
def manage_speaker(): 
    
    # get speaker details
    speaker_id = request.args.get('speaker_id')
    speaker = Speaker.get_by_id(speaker_id) if speaker_id else None
    
    if request.method == 'POST':
        try:
        
            full_name = request.form['full_name']
            bio = request.form['bio']
            email = request.form['email']
            phone_number = request.form['phone_number']
            profile_image = request.form['profile_image']
            
            # create new speaker
            if not speaker:
                
                speaker = Speaker.create(full_name=full_name,
                                    biography=bio,
                                    email=email,
                                    phone_number=phone_number,
                                    profile_image=profile_image)
            else:       
                # update existing speaker
                speaker.update(full_name=full_name,
                            biography=bio,
                            email=email,
                            phone_number=phone_number,
                            profile_image=profile_image)
            
            flash('Speaker saved successfully!', 'success')
            return redirect(url_for('speakers.index'))
                
        except Exception as error:
            flash(str(error), 'error')
            return redirect(url_for('speakers.manage_speaker', speaker_id=speaker.id if speaker else None))
    
    return render_template('speakers.html', speaker=speaker)