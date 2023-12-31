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


users_groups_association_table = db.Table("users_groups_association_table", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"))
)

favorites_likes_association_table = db.Table("favorites_likes_association_table", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)  
    password = db.Column(db.String(256), nullable=False)
    groups = db.relationship("Group", secondary=users_groups_association_table, back_populates="users")
    posts = db.relationship("Post", back_populates="user")
    read = db.Column(db.Boolean, default=True)
    write = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    favorites = db.relationship("Post", secondary=favorites_likes_association_table, back_populates="likes")
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # role = db.Column(db.String(24))
    # comments = db.Column(db.String(128)) # ref to Comment model

    def __str__(self):
            return self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="posts")
    likes = db.relationship("User", secondary=favorites_likes_association_table, back_populates="favorites")
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __str__(self):
        return str(self.id)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship("User", secondary=users_groups_association_table, back_populates="groups")
    read = db.Column(db.Boolean, default=True)
    write = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return self.name

