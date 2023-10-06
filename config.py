import os
from dotenv import load_dotenv
load_dotenv()


mode = os.environ.get("FLASK_ENV")

app_config = None

class Config(object):
    DEBUG = False
    TESTING = False
    BASE_URL = os.environ.get("BASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    BOOTSTRAP_BOOTSWATCH_THEME = os.environ.get("BOOTSTRAP_BOOTSWATCH_THEME")
    FLASK_ADMIN_SWATCH = os.environ.get("FLASK_ADMIN_SWATCH")


class ProductionConfig(Config):
    """Uses production database server."""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")



if mode == "development":
  app_config = DevelopmentConfig()
elif mode == "test":
  app_config = TestingConfig()
elif mode == "production":
  app_config = ProductionConfig()
