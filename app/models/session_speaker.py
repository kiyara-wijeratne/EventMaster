from sqlalchemy import Table, Column, Integer, ForeignKey

from app.models import db

session_speaker = Table(
    'session_speaker',
    db.Model.metadata,
    Column('session_id', Integer, ForeignKey('session.id'), primary_key=True),
    Column('speaker_id', Integer, ForeignKey('speaker.id'), primary_key=True)
)