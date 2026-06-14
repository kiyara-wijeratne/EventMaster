# adapted from
# https://docs.pytest.org/en/stable/getting-started.html
# https://youtu.be/-Vl7006_CnI?si=fYTZ6UL49v9L9mS3

import pytest
from flask import Flask

from app.models import db
from app.models.event_type import EventType
from app.models.role import Role
from app.models.user import User


# https://docs.pytest.org/en/stable/how-to/fixtures.html
@pytest.fixture(scope="session")
def app(config_class="app.config.TestingConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    yield app


# https://flask-sqlalchemy.readthedocs.io/en/stable/contexts/#tests
@pytest.fixture
def app_ctx(app):
    with app.app_context():
        # create the tables
        db.create_all()

        yield

        # close the session
        db.session.close()
        # drop all tables
        db.drop_all()


@pytest.fixture
def seed_workshop_event_type(app_ctx):
    return EventType.create(name="Workshop")


@pytest.fixture
def seed_organiser(app_ctx):
    role = Role.create(name="Organiser")
    return User.create(
        email="organiser@test.com",
        password="password",
        full_name="Test Organiser",
        role_id=role.id,
    )
