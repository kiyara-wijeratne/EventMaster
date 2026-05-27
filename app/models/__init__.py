from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

from app.models.role import Role
from app.models.user import User
from app.models.event_type import EventType
from app.models.event import Event
from app.models.event_branding import EventBranding
from app.models.ticket_type import TicketType
from app.models.registration import Registration
from app.models.check_in import CheckIn
from app.models.session_speaker import session_speaker
from app.models.session import Session
from app.models.speaker import Speaker
from app.models.presentation_material import PresentationMaterial