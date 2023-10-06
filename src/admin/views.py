from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from src.models.models import User
from src.db import db

class UserForm(FlaskForm):
    name = StringField('Name', [Length(min=2, max=128), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3, max=128), DataRequired()])
    admin = SelectField('Role', choices=["user", "admin"], validators=[DataRequired()])
    # posts = StringField('Posts', validators=[DataRequired()])
    # groups = SelectMultipleField('Groups', choices=["group1", "group2", "group3", "group4", "group5", "group6"], validators=[DataRequired()])
    # favorites = StringField('Favorites', validators=[DataRequired()])
    # comments = StringField('Comments')
    # new_comments = StringField('New Comments', validators=[DataRequired()])
    # created = DateField('Created', validators=[DataRequired()])
    # updated = DateField('Updated', validators=[DataRequired()])


class UserModelView(ModelView):
    # form_base_class = SecureForm
    can_create = False
    can_delete = False
    page_size = 20
    # column_list = ['id', 'name', 'email', 'password', 'admin', 'role', 'groups', 'created']
    # form_columns = ('name', 'email', 'password', 'admin', 'role', 'groups')
    column_list = ['id', 'name', 'email', 'read', 'write', 'admin', 'groups', 'favorites', 'created']
    form_columns = ['name', 'email', 'password', 'read', 'write', 'admin', 'groups', 'favorites']
    # form_args = dict(
    #         role=dict(label='Role', choices=['User', 'Admin'],  validators=[DataRequired()])
    #     )
    
    # form = UserForm

    # column_choices = {
    #         'my_column': [
    #             ('db_value', 'display_value'),
    #         ]
    #     }


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    # user_id = SelectField('User', choices=get_users, validators=[DataRequired()])


# class PostForm(FlaskForm):
    
#     @staticmethod
#     def get_users():
#         with app.app_context():
#             with session_db() as session:
#                 return [(str(user.id), user.name) for user in session.query(User).all()]
    
#     title = StringField('Title', validators=[DataRequired()])
#     body = StringField('Body', validators=[DataRequired()])
#     user_id = SelectField('User', choices=get_users, validators=[DataRequired()])
#     created = DateField('Created', validators=[DataRequired()])


class PostModelView(ModelView):
    can_edit = False
    can_create = False
    page_size = 20
    column_list = ['id', 'title', 'body', 'user', 'likes', 'created']
    form_columns = ['title', 'body', 'user']
    # form = PostForm  # Use the custom form class


class GroupForm(FlaskForm):
    
    @staticmethod
    def get_users():
        # with app.app_context():
            with db.session() as session:
                return [(str(user.id), user.name) for user in session.query(User).all()]
    
    name = StringField('Name', validators=[DataRequired()])
    users = SelectMultipleField('Users', choices=get_users, validators=[DataRequired()])
    created = DateField('Created', validators=[DataRequired()])


class GroupModelView(ModelView):
    # can_edit = False
    # can_create = False
    page_size = 20
    column_list = ['id', 'name', 'users', 'read', 'write', 'created']
    form_columns = ['name', 'users', 'read', 'write']
    # form = GroupForm
