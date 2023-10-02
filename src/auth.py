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
    jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
                .filter(User.name == username or User.email == email)
                .first()
            )
            if user_exists:
                if user_exists.name == username:
                    flash("This user is already registered", category="warning")
                    return redirect(url_for("auth.register"))
                elif user_exists.email == email:
                    flash("Choose a different email", category="warning")
                    return redirect(url_for("auth.register"))
            else:
                
                hashed_password = generate_password_hash(password)
                new_user = User(name=username, email=email, password=hashed_password)
                for group_id in selected_groups:
                    new_group = s.query(Group).get(group_id)
                    if new_group:
                        new_user.groups.append(new_group)
                s.add(new_user)
                s.commit()
                flash("User registered successfully!", category="success")
                return redirect(url_for("auth.login"))
    return render_template("auth/register.html", groups=groups)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        with session_db() as s:
            username_exists = s.query(User).filter_by(name=username).first()
            if username_exists is None:
                flash("User is not registered", category="warning")
                # return jsonify({"message": "User is not registered"}, 401)
                return redirect(url_for("auth.login"))
            else:
                user_pass = check_password_hash(username_exists.password, password)
                if not user_pass:
                    flash("Wrong password", category="warning")
                    # return jsonify({"message": "Wrong password"})
                    return redirect(url_for("auth.login"))
                else:
                    session["user"] = username_exists.id
                    token = create_access_token(identity=username)
                    # return jsonify(access_token=token)
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
