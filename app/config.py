# adapted from
# https://flask.palletsprojects.com/en/stable/config/#configuration-basics


class Config(object):
    TESTING = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///eventmaster.db"
    SECRET_KEY = "dev"


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
