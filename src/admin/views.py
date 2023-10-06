from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView

class UserForm(FlaskForm):
    name = StringField('Name', [Length(min=2, max=128), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3, max=128), DataRequired()])
    admin = SelectField('Role', choices=["user", "admin"], validators=[DataRequired()])


class UserModelView(ModelView):
    # form_base_class = SecureForm
    can_create = False
    can_delete = False
    page_size = 20
    column_list = ['id', 'name', 'email', 'read', 'write', 'admin', 'groups', 'favorites', 'created']
    form_columns = ['name', 'email', 'password', 'read', 'write', 'admin', 'groups', 'favorites']


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])


class PostModelView(ModelView):
    can_edit = False
    can_create = False
    page_size = 20
    column_list = ['id', 'title', 'body', 'user', 'likes', 'created']
    form_columns = ['title', 'body', 'user']


class GroupModelView(ModelView):
    page_size = 20
    column_list = ['id', 'name', 'users', 'read', 'write', 'created']
    form_columns = ['name', 'users', 'read', 'write']
