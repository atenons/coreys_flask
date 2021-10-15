from flask import render_template, redirect, flash, url_for, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment
from app.posts.forms import PostForm, CommentForm

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash("Post has been created!", "success")
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)

    form = CommentForm()

    if request.method == "POST":
        comment = Comment(
            content=form.content.data, post_id=post_id, author=current_user
        )
        if form.validate_on_submit():

            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("posts.post", post_id=post.id))

    return render_template("post.html", title=post.title, post=post, form=form)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post has been update!", "success")
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    for comment in post.comments:
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    flash("Post has been deleted!", "success")
    return redirect(url_for("main.home"))


@posts.route(
    "/post/<int:post_id>/<int:comment_id>/delete_comment", methods=["GET", "POST"]
)
@login_required
def delete_comment(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    if current_user != comment.author:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("posts.post", post_id=post.id))
