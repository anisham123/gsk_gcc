from os import environ, path

from dotenv import load_dotenv




class Config:
    """Base config."""

    SECRET_KEY =  b'\x8d\xa8\x1a;jvx\xd1p+\xbbC\xed\xf1I\x10\xa2\xa1$Yd\x8c\xf2U'
    SESSION_COOKIE_NAME = 'secret_cookie'
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Assets related config
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = True

    # Custom User configuration
    USER_CONFIG = {}

    def set_user_config(self, config):
        assert isinstance(config, dict)
        # TODO : Add JSON schema validation - only acceptable config values should be saved
        self.USER_CONFIG = config

    def get_user_config(self):
        return self.USER_CONFIG


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    # DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    # DATABASE_URI = environ.get('DEV_DATABASE_URI')
