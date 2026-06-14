from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db


# adapted from
# https://flask-sqlalchemy.readthedocs.io/en/stable/models/
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
class EventBranding(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    logo_path: Mapped[Optional[str]] = mapped_column(String(255))
    primary_colour: Mapped[Optional[str]] = mapped_column(String(7))
    secondary_colour: Mapped[Optional[str]] = mapped_column(String(7))

    event: Mapped["Event"] = relationship(back_populates="branding")

    # adapted from
    # https://stackoverflow.com/questions/35814211/how-to-add-a-custom-function-method-in-sqlalchemy-model-to-do-crud-operations
    # https://flask-sqlalchemy.readthedocs.io/en/stable/queries/
    @classmethod
    def create(cls, event_id, logo_path, primary_colour, secondary_colour):
        event_branding = cls(
            event_id=event_id,
            logo_path=logo_path,
            primary_colour=primary_colour,
            secondary_colour=secondary_colour,
        )
        db.session.add(event_branding)
        db.session.commit()
        return event_branding

    @classmethod
    def get_by_event_id(cls, event_id):
        return db.session.execute(
            db.select(cls).filter_by(event_id=event_id)
        ).scalar_one_or_none()

    def update(self, logo_path=None, primary_colour=None, secondary_colour=None):
        if logo_path:
            self.logo_path = logo_path
        if primary_colour:
            self.primary_colour = primary_colour
        if secondary_colour:
            self.secondary_colour = secondary_colour
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
