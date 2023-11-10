import os


mode = os.environ.get("FLASK_ENV")

app_config = None

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


class ProductionConfig(Config):
    """Uses production database server."""
    BASE_URL = os.environ.get("BASE_URL")
    BOOTSTRAP_BOOTSWATCH_THEME = os.environ.get("BOOTSTRAP_BOOTSWATCH_THEME")
    FLASK_ADMIN_SWATCH = os.environ.get("FLASK_ADMIN_SWATCH")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = os.environ.get("DEV_BASE_URL")
    BOOTSTRAP_BOOTSWATCH_THEME = os.environ.get("DEV_BOOTSTRAP_BOOTSWATCH_THEME")
    FLASK_ADMIN_SWATCH = os.environ.get("DEV_FLASK_ADMIN_SWATCH")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")
    
    
class TestingConfig(Config):
    TESTING = True
    BASE_URL = os.environ.get("TEST_BASE_URL")
    BOOTSTRAP_BOOTSWATCH_THEME = os.environ.get("TEST_BOOTSTRAP_BOOTSWATCH_THEME")
    FLASK_ADMIN_SWATCH = os.environ.get("TEST_FLASK_ADMIN_SWATCH")
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")


def get_config(mode):
  if mode == "production":
    app_config = ProductionConfig()
  elif mode == "development":
    app_config = DevelopmentConfig()
  elif mode == "test":
    app_config = TestingConfig()
  return app_config
