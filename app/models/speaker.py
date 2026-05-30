from typing import List, Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
from app.models.session_speaker import session_speaker
 
class Speaker(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    biography: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    profile_image: Mapped[Optional[str]] = mapped_column(String(255))
 
    sessions: Mapped[List["Session"]] = relationship(secondary=session_speaker, back_populates="speakers")
    materials: Mapped[List["PresentationMaterial"]] = relationship(back_populates="speaker")
    
    @classmethod
    def create(cls, full_name, biography, email, phone_number, profile_image):
        speaker = cls(full_name=full_name,
                      biography=biography,
                      email=email,
                      phone_number=phone_number,
                      profile_image=profile_image)
        db.session.add(speaker)
        db.session.commit()
        return speaker
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    def update(self, full_name=None, biography=None, email=None, phone_number=None, profile_image=None):
        if full_name:
            self.full_name = full_name
        if biography:
            self.biography = biography
        if email:
            self.email = email
        if phone_number:
            self.phone_number = phone_number
        if profile_image:
            self.profile_image = profile_image
        
        db.session.commit()
        return self