from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# adapted from
# https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# adapted from
# https://stackoverflow.com/questions/75290501/is-it-possible-to-use-sqlalchemy-where-the-models-are-defined-in-different-files
from app.models.check_in import CheckIn
from app.models.event import Event
from app.models.event_branding import EventBranding
from app.models.event_type import EventType
from app.models.presentation_material import PresentationMaterial
from app.models.registration import Registration
from app.models.role import Role
from app.models.session import Session
from app.models.session_speaker import session_speaker
from app.models.speaker import Speaker
from app.models.ticket_type import TicketType
from app.models.user import User
