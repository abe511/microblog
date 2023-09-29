import os

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from src import auth, blog, db
from src.models.models import User, Post, Group, session_db
from flask_admin import Admin
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView

from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SelectMultipleField, TimeField
from wtforms.validators import DataRequired, Length


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="src/templates",
        static_folder="src/static",
    )
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    # ] = "postgresql://postgres:password@localhost:5434/flask_db"
    ] = "postgresql://postgres:postgres@localhost:5433/flask_db"
    app.config["SQLALCHEMY_SESSION_OPTIONS"] = {"expire_on_commit": False}
    app.config["SECRET_KEY"] = "your_secret_key_here"

    app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "slate"
    app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    
    db.init_app(app)

    bootstrap = Bootstrap5(app)
    admin = Admin(app, name='microblog', template_mode='bootstrap3')


    # app.config["IPYTHON_CONFIG"] = {
    #     "InteractiveShell": {
    #         "colors": "Linux",
    #         "confirm_exit": False,
    #     },
    # }

    # **************
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # **************
    

    @app.route("/hello")
    def hello():
        return "Hello, World!"


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
            with app.app_context():
                with session_db() as session:
                    return [(str(user.id), user.name) for user in session.query(User).all()]
        
        name = StringField('Name', validators=[DataRequired()])
        users = SelectMultipleField('Users', choices=get_users, validators=[DataRequired()])
        created = DateField('Created', validators=[DataRequired()])


    class GroupModelView(ModelView):
        # can_edit = False
        # can_create = False
        page_size = 20
        column_list = ['id', 'name', 'users', 'read', 'write', 'created']
        form_columns = ['name', 'users']
        # form = GroupForm




    admin.add_view(PostModelView(Post, db.session))
    admin.add_view(UserModelView(User, db.session))
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Group, db.session))
    admin.add_view(GroupModelView(Group, db.session))


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
