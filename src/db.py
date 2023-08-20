from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
migrate = Migrate()


def init_app(app):
    from src.models.models import User, Posts

    db.init_app(app)
    migrate.init_app(app, db)
