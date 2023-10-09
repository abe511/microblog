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

from flask_jwt_extended import jwt_required, get_jwt_identity, get_csrf_token

from src.models.models import session_db, Post, User


bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    user_id = session.get("user")
    if user_id is not None:
        return redirect(url_for("blog.feed"))
    
    with session_db() as s:
        posts = s.query(Post).order_by(Post.created.desc()).all()
    return render_template("blog/index.html", posts=posts)


@bp.route("/feed/")
@bp.route("/favorites/", endpoint="favorites")
@jwt_required()
def feed():
    user_id = get_jwt_identity()
    session["user"] = user_id
    posts = []
    favorites = []
    if user_id is None:
        return redirect(url_for("blog.index"))
    else:
        with session_db() as s:
            user = s.query(User).get(user_id)
            g.user = user
            favorites = user.favorites
            if not user.groups and user.posts:
                posts.extend(reversed(user.posts))
            else:
                users_from_groups = []
                for group in user.groups:
                    users_from_groups.extend(group.users)
                
                user_ids = []
                for group_user in users_from_groups:
                    user_ids.append(group_user.id)

                query = s.query(Post).join(Post.user).filter(User.id.in_(user_ids))
                posts = query.order_by(Post.created.desc()).all()
    if request.path == "/favorites/":
        return render_template("blog/feed.html", posts=favorites, favorites=favorites)
    return render_template("blog/feed.html", posts=posts, favorites=favorites)


@bp.route("/create", methods=("GET", "POST"))
@jwt_required()
def create():
    # encoded = request.cookies.get("access_token")
    # csrf_token = get_csrf_token(encoded)
    user_id = get_jwt_identity()
    with session_db() as s:
        g.user = s.query(User).get(user_id)
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        with session_db() as s:
            new_post = Post(title=title, body=body, user_id=user_id)
            s.add(new_post)
            s.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")
    # return render_template("blog/create.html", csrf_token=csrf_token)


def get_post(id, check_author=True):
    user_id = session.get("user")
    post = None
    with session_db() as s:
        g.user = s.query(User).get(user_id)
        for user_post in g.user.posts:
            if user_post.id == id:
                post = user_post

        if post is None:
            abort(404, f"Post id {id} doesn't exist.")

        if check_author and post.user_id != g.user.id:
            abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@jwt_required()
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
@jwt_required()
def delete(id):
    get_post(id)
    with session_db() as s:
        s.query(Post).filter(Post.id == id).delete()
        s.commit()
    return redirect(url_for("blog.index"))


@bp.route("/like_post/<int:post_id>", methods=["POST"])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()

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
