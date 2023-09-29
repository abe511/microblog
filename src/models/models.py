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
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)  
    password = db.Column(db.String(128))
    groups = db.relationship("Group", secondary=users_groups_association_table, back_populates="users")
    posts = db.relationship("Post", back_populates="user")
    read = db.Column(db.Boolean, default=True)
    write = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    favorites = db.relationship("Post", secondary=favorites_likes_association_table, back_populates="likes")
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    role = db.Column(db.String(24))

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

    def __str__(self):
        return self.title
    
    def like(self, user):
        users = self.likes
        print(users)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), unique=True)
#     email = db.Column(db.String(128), unique=True)
#     password = db.Column(db.String(128))
#     role = db.Column(db.String(24))
#     # posts = db.relationship("Post", backref="user", lazy=True)
#     posts = db.relationship("Post", back_populates="user")
#     groups = db.relationship("Group", secondary=users_groups_association_table, back_populates="users")
#     favorites = db.relationship("Post", secondary=favorites_likes_association_table, back_populates="likes")
#     comments = db.Column(db.String(128)) # ref to Comment model
#     created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     # updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#     # def __str__(self):
#     #         return self.name

#     def add_user_to_group(self, group):
#         try:
#             if group not in self.groups:
#                 self.group.append(group)
#                 db.session.commit()
#         except SQLAlchemyError as e:
#             print(e)

#     def remove_user_from_group(self, group):
#         try:
#             if group in self.groups:
#                 self.groups.remove(group)
#                 db.session.commit()
#         except SQLAlchemyError as e:
#             print(e)

# backref="user" = user field automatically added to represent creator of the post
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     body = db.Column(db.Text)
#     user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
#     user = db.relationship("User", back_populates="posts")
#     likes = db.relationship("User", secondary=favorites_likes_association_table, back_populates="favorites")
#     created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     # updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)





class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship("User", secondary=users_groups_association_table, back_populates="groups")
    read = db.Column(db.Boolean, default=True)
    write = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # # updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
            return self.name

    # def list_groups(self):
    #     ...
    
    # def add_group(self, data):
    #     ...

    # def edit_group(self, group, data):
    #     ...
    
    # def remove_group(self, group):
    #     ...