from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db
 
class CheckIn(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    registration_id: Mapped[int] = mapped_column(ForeignKey('registration.id'))
    coordinator_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
 
    registration: Mapped["Registration"] = relationship(back_populates="check_in")
    coordinator: Mapped["User"] = relationship(back_populates="check_ins_managed")
    
    @classmethod
    def create(cls, registration_id, coordinator_id):  
        check_in = cls(registration_id=registration_id,
                           coordinator_id=coordinator_id)
            
        db.session.add(check_in)
        db.session.commit()
        return check_in
    
    @classmethod
    def get_by_registration_id(cls, registration_id):
        return db.session.execute(db.select(cls).filter_by(registration_id=registration_id)).scalar_one_or_none()