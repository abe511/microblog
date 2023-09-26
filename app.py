import os

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField

from src import auth, blog, db
from src.models.models import User, Posts, session_db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_bootstrap import Bootstrap5


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

    bootstrap = Bootstrap5(app)
    
    db.init_app(app)

    app.config["IPYTHON_CONFIG"] = {
        "InteractiveShell": {
            "colors": "Linux",
            "confirm_exit": False,
        },
    }

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


    admin = Admin(app, name='microblog', template_mode='bootstrap3')

    from flask_wtf import FlaskForm
    from wtforms import SelectField, DateField
    from wtforms.validators import DataRequired

    class PostForm(FlaskForm):

        title = StringField('Title', validators=[DataRequired()])
        body = StringField('Body', validators=[DataRequired()])
        user_id = SelectField('User', choices=[1,2,3], validators=[DataRequired()])
        created = DateField('Created', validators=[DataRequired()])

    class PostAdminView(ModelView):
        column_list = ['id', 'title', 'body', 'user_id', 'created']
        form = PostForm  # Use the custom form class


    admin.add_view(PostAdminView(Posts, db.session))
    admin.add_view(ModelView(User, db.session))


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
