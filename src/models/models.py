from contextlib import contextmanager
import datetime

from sqlalchemy.exc import SQLAlchemyError

from src.db import db


@contextmanager
def session_db():
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise e




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship("Posts", backref="user", lazy=True)
    comments = db.Column(db.String(128))
    new_comments = db.Column(db.String(128))




class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)




