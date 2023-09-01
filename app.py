import os

from flask import Flask

from src import auth, blog, db

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
    ] = "postgresql://postgres:password@localhost:5434/flask_db"
    app.config["SQLALCHEMY_SESSION_OPTIONS"] = {"expire_on_commit": False}
    app.config["SECRET_KEY"] = "your_secret_key_here"

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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
