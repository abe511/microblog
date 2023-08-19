from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Remove this line if you already have an instance


def init_app(app):
    db.init_app(app)
