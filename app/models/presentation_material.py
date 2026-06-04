from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class PresentationMaterial(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    speaker_id: Mapped[int] = mapped_column(ForeignKey('speaker.id'))
    session_id: Mapped[int] = mapped_column(ForeignKey('session.id'))
    file_path: Mapped[str] = mapped_column(String(255))
 
    speaker: Mapped["Speaker"] = relationship(back_populates="materials")
    session: Mapped["Session"] = relationship(back_populates="materials")
    
    @classmethod
    def create(cls, speaker_id, session_id, file_path):
        presentation_material = cls(speaker_id=speaker_id,
                                    session_id=session_id,
                                    file_path=file_path)
        db.session.add(presentation_material)
        db.session.commit()
        return presentation_material
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    @classmethod
    def get_by_session_id(cls, session_id):
        return db.session.execute(db.select(cls).filter_by(session_id=session_id)).scalars().all()
    
    def update(self, file_path):
        self.file_path = file_path
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()