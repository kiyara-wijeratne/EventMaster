from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import db


# adapted from
# https://flask-sqlalchemy.readthedocs.io/en/stable/models/
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
class CheckIn(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    registration_id: Mapped[int] = mapped_column(ForeignKey("registration.id"))
    coordinator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    registration: Mapped["Registration"] = relationship(back_populates="check_in")
    coordinator: Mapped["User"] = relationship(back_populates="check_ins_managed")

    # adapted from
    # https://stackoverflow.com/questions/35814211/how-to-add-a-custom-function-method-in-sqlalchemy-model-to-do-crud-operations
    # https://flask-sqlalchemy.readthedocs.io/en/stable/queries/
    @classmethod
    def create(cls, registration_id, coordinator_id):
        check_in = cls(registration_id=registration_id, coordinator_id=coordinator_id)

        db.session.add(check_in)
        db.session.commit()
        return check_in

    @classmethod
    def get_by_registration_id(cls, registration_id):
        return db.session.execute(
            db.select(cls).filter_by(registration_id=registration_id)
        ).scalar_one_or_none()
