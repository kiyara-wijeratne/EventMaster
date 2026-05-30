from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
from app.models.session_speaker import session_speaker
 
class Session(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.id'))
    title: Mapped[str] = mapped_column(String(150))
    session_start: Mapped[datetime] = mapped_column(DateTime)
    session_end: Mapped[datetime] = mapped_column(DateTime)
    room: Mapped[str] = mapped_column(String(100))
 
    event: Mapped["Event"] = relationship(back_populates="sessions")
    speakers: Mapped[List["Speaker"]] = relationship(secondary=session_speaker, back_populates="sessions")
    materials: Mapped[List["PresentationMaterial"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    
    @classmethod
    def create(cls, event_id, title, session_start, session_end, room):
        # validate session starts before the end time
        if session_start >= session_end:
            raise ValueError("Session end time must be after the start time.")
        
        # validate session falls within event timings
        from app.models.event import Event
        event = Event.get_by_id(event_id)
        if session_start < event.event_start or session_end > event.event_end:
            raise ValueError("Session time must fall within main event hours.")
        
        session = cls(event_id=event_id,
                      title=title,
                      session_start=session_start, 
                      session_end=session_end,
                      room=room)
        db.session.add(session)
        db.session.commit()
        return session
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    def add_speaker(self, speaker_id):
        from app.models.speaker import Speaker 
        speaker = Speaker.get_by_id(speaker_id)
        
        # validate speaker exists
        if not speaker:
            raise ValueError("Speaker not found")
        
        # validate speaker not already added to session
        if speaker in self.speakers:
            return self
        
        self.speakers.append(speaker)
        db.session.commit()
        return self
    
    def remove_speaker(self, speaker_id):
        from app.models.speaker import Speaker
        speaker = Speaker.get_by_id(speaker_id)
        
        # validate speaker exists
        if not speaker:
            raise ValueError("Speaker not found")
        
        # validate speaker is added to session
        if speaker not in self.speakers:
            raise ValueError("Speaker not assigned to the session.")
        
        self.speakers.remove(speaker)
        
        # delete any linked presentation materials
        from app.models.presentation_material import PresentationMaterial
        presentation_materials = db.session.execute(
            db.select(PresentationMaterial).
            filter_by(session_id=self.id,
                      speaker_id=speaker.id)).scalars().all()
        
        for material in presentation_materials:
            db.session.delete(material)
            
        db.session.commit()
        return self
    
    def update(self, title=None, room=None):
        if title:
            self.title = title
        if room:
            self.room = room
        return self
    
    def reschedule(self, new_start, new_end):
        from app.models.event import Event
        event = Event.get_by_id(self.event_id)
        
        # validate session starts before the end time
        if new_start >= new_end:
            raise ValueError("Session end time must be after the start time.")
        
        # validate session falls within event timings
        if new_start < event.event_start or new_end > event.event_end:
            raise ValueError("Session time must fall within main event hours.")
        
        self.session_start = new_start
        self.session_end = new_end
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()