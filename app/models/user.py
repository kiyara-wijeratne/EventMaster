from typing import List

from flask_login import UserMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import db


# adapted from
# https://flask-sqlalchemy.readthedocs.io/en/stable/models/
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
# https://medium.com/@mathur.danduprolu/user-authentication-and-authorization-in-flask-building-secure-login-and-access-control-part-5-7-59679a08cdc3
class User(db.Model, UserMixin):  # implements necessary methods for flask_login
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    role: Mapped["Role"] = relationship(back_populates="users")
    organised_events: Mapped[List["Event"]] = relationship(back_populates="organiser")
    registrations: Mapped[List["Registration"]] = relationship(
        back_populates="attendee"
    )
    check_ins_managed: Mapped[List["CheckIn"]] = relationship(
        back_populates="coordinator"
    )

    # adapted from
    # https://stackoverflow.com/questions/35814211/how-to-add-a-custom-function-method-in-sqlalchemy-model-to-do-crud-operations
    # https://flask-sqlalchemy.readthedocs.io/en/stable/queries/
    # https://www.youtube.com/watch?v=jJ4awOToB6k&t=8s
    @classmethod
    def create(cls, email, password, full_name, role_id):
        # validate email is unique
        if cls.get_by_email(email) is not None:
            raise ValueError(f"An account with this email already exists.")

        password_hash = generate_password_hash(password)
        user = cls(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role_id=role_id,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)

    @classmethod
    def get_by_email(cls, email):
        return db.session.execute(
            db.select(cls).filter_by(email=email)
        ).scalar_one_or_none()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def assign_role(self, new_role_id):
        from app.models.role import Role

        # validate new_role_id is valid
        if Role.get_by_id(new_role_id) is None:
            raise ValueError("Cannot assign role: The requested role does not exist.")

        self.role_id = new_role_id
        db.session.commit()
        return self
