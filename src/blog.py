from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    session,
    jsonify,
)
from werkzeug.exceptions import abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.models import session_db, Post, User, Group, users_groups_association_table
from src.auth import login_required


bp = Blueprint("blog", __name__)


@bp.route("/")
@bp.route("/favorites/", endpoint="favorites")
# @jwt_required()
def index():
    # current_user = get_jwt_identity()
    # print("current user:", current_user)
    favorites = []
    user_id = session.get("user")
    if user_id is None:
        with session_db() as s:
            posts = s.query(Post).order_by(Post.created.desc()).all()
    else:
        with session_db() as s:
            user = s.query(User).get(user_id)
            other_group_users = []
            for group in user.groups:
                other_group_users.extend(group.users)
            
            user_ids = []
            for group_user in other_group_users:
                user_ids.append(group_user.id)

            query = s.query(Post).join(Post.user).filter(User.id.in_(user_ids))
            posts = query.order_by(Post.created.desc()).all()
            favorites = user.favorites
    if request.path == "/favorites/":
        return render_template("blog/index.html", posts=favorites, favorites=favorites)
    return render_template("blog/index.html", posts=posts, favorites=favorites)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        user_id = session.get("user")
        print("user_id from BLOG", user_id)

        with session_db() as s:
            new_post = Post(title=title, body=body, user_id=user_id)
            s.add(new_post)
            s.commit()

            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")


def get_post(id, check_author=True):
    with session_db() as s:
        query = s.query(Post)
        query = query.join(User, User.id == Post.user_id)
        post = query.filter(Post.id == id).first()

        if post is None:
            abort(404, f"Post id {id} doesn't exist.")

        if check_author and post.user_id != g.user.id:
            abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            with session_db() as s:
                post = s.query(Post).get(id)
                post.body = body
                post.title = title
                s.commit()
                return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    get_post(id)
    with session_db() as s:
        s.query(Post).filter(Post.id == id).delete()
        s.commit()
    return redirect(url_for("blog.index"))


@bp.route("/like_post/<int:post_id>", methods=["POST"])
def like_post(post_id):
    user_id = session.get("user")

    with session_db() as s:
        user = s.query(User).get(user_id)
        post = s.query(Post).get(post_id)
        
        if post:
            if user in post.likes:
                post.likes.remove(user)
                s.commit()
                return jsonify({"message": "Unliked"})
            else:
                post.likes.append(user)
                s.commit()
                return jsonify({"message": "Liked"})
        return jsonify({"message": "Error"})
