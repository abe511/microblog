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

users_favorites_association_table = db.Table("users_favorites_association_table", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(24))
    posts = db.relationship("Post", backref="user", lazy=True)
    groups = db.relationship("Group", secondary=users_groups_association_table, back_populates="users")
    favorites = db.relationship("Post", secondary=users_favorites_association_table, back_populates="users")
    comments = db.Column(db.String(128))
    new_comments = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def add_user_to_group(self, group):
        try:
            if group not in self.groups:
                self.group.append(group)
                db.session.commit()
        except SQLAlchemyError as e:
            print(e)

    def remove_user_from_group(self, group):
        try:
            if group in self.groups:
                self.groups.remove(group)
                db.session.commit()
        except SQLAlchemyError as e:
            print(e)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)
    likes = db.relationship("User", secondary=users_favorites_association_table, back_populates="post")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship("User", secondary=users_groups_association_table, back_populates="groups")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def list_groups(self):
        ...
    
    def add_group(self, data):
        ...

    def edit_group(self, group, data):
        ...
    
    def remove_group(self, group):
        ...