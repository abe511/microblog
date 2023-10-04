import os
from dotenv import load_dotenv
load_dotenv()


env = dict(os.environ.items())

mode = env.get("FLASK_ENV")

app_config = None

class Config(object):
    DEBUG = False
    TESTING = False
    BASE_URL = env.get("BASE_URL")
    SECRET_KEY = env.get("SECRET_KEY")
    JWT_SECRET_KEY = env.get("JWT_SECRET_KEY")
    BOOTSTRAP_BOOTSWATCH_THEME = env.get("BOOTSTRAP_BOOTSWATCH_THEME")
    FLASK_ADMIN_SWATCH = env.get("FLASK_ADMIN_SWATCH")

    # @property
    # def DATABASE_URI(self):  # Note: all caps
    #     return f"mysql://user@{self.DB_SERVER}/foo"

class ProductionConfig(Config):
    """Uses production database server."""
    SQLALCHEMY_DATABASE_URI = env.get("DATABASE_URI")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env.get("DEV_DATABASE_URI")
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = env.get("TEST_DATABASE_URI")


if mode == "development":
  app_config = DevelopmentConfig()
elif mode == "testing":
  app_config = TestingConfig()
elif mode == "production":
  app_config = ProductionConfig()
