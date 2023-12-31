import datetime

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    make_response,
    request,
    session,
    url_for,
    jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    unset_access_cookies,
    get_csrf_token,
    create_refresh_token,
    set_refresh_cookies,
)
from src.models.models import session_db, User, Group


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if session.get("user"):
        return redirect(url_for("blog.feed"))
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
    if session.get("user"):
        return redirect(url_for("blog.feed"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        with session_db() as s:
            user_exists = s.query(User).filter_by(name=username).first()
            if user_exists is None:
                flash("User is not registered", category="warning")
                # return jsonify({"message": "User is not registered"}, 401)
                return redirect(url_for("auth.login"))
            else:
                password_match = check_password_hash(user_exists.password, password)
                if not password_match:
                    
                    flash("Wrong password", category="warning")
                    # return jsonify({"message": "Wrong password"})
                    return redirect(url_for("auth.login"))
                else:
                    # session["user"] = user_exists.id
                    response = make_response(redirect(url_for("blog.feed")))
                    
                    # TODO: add "role" to identity
                    # identity = {"id": user_exists.id, "role": "user"}
                    # if user_exists.admin:
                    #     identity["role"] = "admin"
                    # access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(minutes=20))
                    
                    access_token = create_access_token(identity=user_exists.id, expires_delta=datetime.timedelta(minutes=20))
                    refresh_token = create_refresh_token(identity=user_exists.id)
                    set_access_cookies(response, access_token)
                    set_refresh_cookies(response, refresh_token)
                    # csrf_token = get_csrf_token(access_token)
                    # response.headers["X-CSRF-TOKEN"] = csrf_token
                    set_access_cookies(response, access_token)                    
                    return response
                    # return jsonify(access_token=access_token)
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    response = redirect(url_for("blog.index"))
    unset_jwt_cookies(response)
    session.clear()
    return response


# @jwt.unauthorized_loader
# def unauthorized_callback(callback):
#     # No auth header
#     return redirect(app.config["BASE_URL"] + '/signup', 302)
#     # return redirect(BASE_URL + '/signup', 302)

# @jwt.invalid_token_loader
# def invalid_token_callback(callback):
#     # Invalid Fresh/Non-Fresh Access token in auth header
#     resp = make_response(redirect(app.config["BASE_URL"] + '/signup'))
#     unset_jwt_cookies(resp)
#     return resp, 302


# @jwt.expired_token_loader
# def expired_token_callback(callback):
#     # Expired auth header
#     resp = make_response(redirect(app.config["BASE_URL"] + '/token/refresh'))
#     unset_access_cookies(resp)
#     return resp, 302