import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from src.models.models import session_db, User, Posts

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with session_db() as s:
            exist_user = (
                s.query(User)
                .filter(User.name == username, User.password == password)
                .first()
            )
            if exist_user:
                session["user"] = exist_user.id

                return redirect(url_for("auth.login"))
            else:
                new_user = User(name=username, password=password)
                s.add(new_user)
                s.commit()
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with session_db() as s:
            exist_user = (
                s.query(User)
                .filter(User.name == username, User.password == password)
                .first()
            )
            session["user"] = exist_user.id

            if not exist_user:
                return redirect(url_for("auth.register"))

        return redirect(url_for("blog.index"))
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user")
    if user_id is None:
        g.user = None
    else:
        with session_db() as s:
            g.user = s.query(User).get(user_id)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("blog.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
