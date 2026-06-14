from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models import db

# adapted from
# https://flask-sqlalchemy.readthedocs.io/en/stable/models/
# https://docs.sqlalchemy.org/en/20/core/metadata.html
session_speaker = Table(
    "session_speaker",
    db.Model.metadata,
    Column("session_id", Integer, ForeignKey("session.id"), primary_key=True),
    Column("speaker_id", Integer, ForeignKey("speaker.id"), primary_key=True),
)
