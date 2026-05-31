from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db

class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    
    users: Mapped[List["User"]] = relationship(back_populates="role")
    
    @classmethod
    def create(cls, name):
        # validate role is unique
        if cls.get_by_name(name) is not None:
            raise ValueError(f"Role '{name}' already exists.")
        
        role = cls(name=name)
        db.session.add(role)
        db.session.commit()
        return role
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)
    
    @classmethod
    def get_by_name(cls, name):
        return db.session.execute(db.select(cls).filter_by(name=name)).scalar_one_or_none()