
from .models import Post
from flask import url_for, render_template, flash, redirect, current_app
from .. import db
from flask_login import current_user, login_required
import os
import secrets
from .forms import CreatePostForm

from . import post_blueprint
from PIL import Image


@post_blueprint.route('/', methods=['GET', 'POST'])
def view_post():
    all_posts = Post.query.all()
    image_file = url_for('static', filename='posts_pics/')
    return render_template('posts.html', posts=all_posts, image_file=image_file)


@post_blueprint.route('/<pk>', methods=['GET', 'POST'])
def view_detail(pk):
    get_post = Post.query.get_or_404(pk)
    return render_template('detail.html', post=get_post)


@post_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image = picture_file
        else:
            image = 'postdefault.jpg'

        post = Post(title=form.title.data, text=form.text.data, type=form.type.data, image_file=image,
                     post_id=current_user.id)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('post.view_post'))

    return render_template('create.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/posts_pics', picture_fn)
    output_size = (250, 250)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@post_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
def delete_post(id):
    get_post = Post.query.get_or_404(id)
    if current_user.id == get_post.post_id:
        db.session.delete(get_post)
        db.session.commit()
        return redirect(url_for('post.view_post'))

    flash('This is not your post', category='warning')
    return redirect(url_for('post.view_detail', pk=id))


@post_blueprint.route('/update/<id>', methods=['GET', 'POST'])
def update_post(id):
    get_post = Post.query.get_or_404(id)
    if current_user.id != get_post.post_id:
        flash('This is not your post', category='warning')
        return redirect(url_for('post.view_detail', pk=id))

    form = CreatePostForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            get_post.image_file = picture_file

        get_post.title = form.title.data
        get_post.text = form.text.data
        get_post.type = form.type.data

        db.session.commit()
        db.session.add(get_post)

        flash('You post has been update', category='access')
        return redirect(url_for('post.view_detail', pk=pk))

    form.title.data = get_post.title
    form.text.data = get_post.text
    form.type.data = get_post.type

    return render_template('create.html', form=form)