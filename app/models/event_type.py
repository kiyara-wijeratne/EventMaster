from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class EventType(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    
    events: Mapped[List["Event"]] = relationship(back_populates="event_type")
    
    @classmethod
    def create(cls, name):
        # validate event type name is unique
        if cls.get_by_name(name) is not None:
            raise ValueError(f"Event type '{name}' already exists")
        
        event_type = cls(name=name)
        db.session.add(event_type)
        db.session.commit()
        return event_type
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    @classmethod
    def get_by_name(cls, name):
        return db.session.execute(db.select(cls).filter_by(name=name)).scalar_one_or_none()