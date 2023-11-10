import os
from config import get_config
from flask import Flask
from flask_admin import Admin
from flask_alembic import Alembic
from flask_bootstrap import Bootstrap5
from flask_jwt_extended import JWTManager
from src import auth, blog, db
from src.admin.views import GroupModelView, PostModelView, UserModelView
from src.models.models import Group, Post, User
from dotenv import load_dotenv


def create_app(mode=None):
    load_dotenv()
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

    app.config.from_object(get_config(mode or os.environ.get("FLASK_ENV")))

    print("mode:", mode)
    print("app cfg:", app.config)
    
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
            login = app.config["ADMIN_USERNAME"]
            email = app.config["ADMIN_EMAIL"]
            password = app.config["ADMIN_PASSWORD"]
            user = User(name=login, email=email, password=password)
            user.admin = True
            db.session.add(user)
            db.session.commit()
    
    admin = Admin(app, name="dashboard", template_mode="bootstrap4")
    admin.add_view(PostModelView(Post, db.session))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(GroupModelView(Group, db.session))

    return app

