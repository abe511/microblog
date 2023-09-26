from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
session = db.session
migrate = Migrate()


def init_app(app):
    from src.models.models import User, Post, Group
    db.init_app(app)
    migrate.init_app(app, db)
