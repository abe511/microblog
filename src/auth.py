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

from src.models.models import session_db, User, Post, Group

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    with session_db() as s:
        groups = s.query(Group).all()
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        selected_groups = request.form.getlist("groups")

        with session_db() as s:
            user_exists = (
                s.query(User)
                # .filter(User.name == username or User.email == email, User.password == password)
                .filter(User.name == username or User.email == email)
                .first()
            )
            if user_exists:
                session["user"] = user_exists.id
                flash("This user is already registered!", "warning")
                return redirect(url_for("auth.login"))
            else:
                new_user = User(name=username, email=email, password=password)
                for group_id in selected_groups:
                    new_group = s.query(Group).get(group_id)
                    if new_group:
                        new_user.groups.append(new_group)
                s.add(new_user)
                s.commit()
                flash("User registered successfully!", "success")
                return redirect(url_for("auth.login"))
    return render_template("auth/register.html", groups=groups)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with session_db() as s:
            user_exists = (
                s.query(User)
                .filter(User.name == username, User.password == password)
                .first()
            )
            session["user"] = user_exists.id

            if not user_exists:
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
