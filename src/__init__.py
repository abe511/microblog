import os
from config import app_config
from flask import Flask
from flask_admin import Admin
from flask_alembic import Alembic
from flask_bootstrap import Bootstrap5
from flask_jwt_extended import JWTManager
from src import auth, blog, db
from src.admin.views import GroupModelView, PostModelView, UserModelView
from src.models.models import Group, Post, User


def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates",
        static_folder="static",
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_object(app_config)

    app.config["SQLALCHEMY_SESSION_OPTIONS"] = {"expire_on_commit": False}
    app.config["JWT_TOKEN_LOCATION"] = "cookies"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    alembic = Alembic()
    alembic.init_app(app)

    # from db module run custom init_app function
    db.init_app(app)
    
    JWTManager(app)

    Bootstrap5(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    
    # create all tables and admin user on first run
    with app.app_context():
        db.db.create_all()
        admin_exists = db.session.query(User).get(1)
        if admin_exists is None:  
            user = User(name="admin", email="admin@server.net", password="admin")
            user.admin = True
            db.session.add(user)
            db.session.commit()
    
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(PostModelView(Post, db.session))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(GroupModelView(Group, db.session))

    return app

