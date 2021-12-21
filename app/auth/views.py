import os
import secrets
from datetime import datetime

from PIL import Image
from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask_login import login_user, current_user, logout_user, login_required

from .models import User
from .. import db, bcrypt
from . import auth_blueprint
from .forms import SignUpForm, LoginForm, UpdateAccountForm, ResetPasswordForm


@auth_blueprint.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index.html"))
    registration = SignUpForm()
    if registration.validate_on_submit():
        user = User(username=registration.username.data, email=registration.email.data,
                    password=registration.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {registration.username.data} !', category='success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', registration=registration)


@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.verify_password(login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            flash(f'You have been logged by email {user.email}!', category='success')
            return redirect(url_for('auth.account'))
        else:
            flash('Invalid login or password!', category='warning')
            return redirect(url_for('auth.login'))

    return render_template('login.html', login_form=login_form)


@auth_blueprint.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    users_list = User.query.all()
    users_amount = User.query.count()
    if users_amount == 0:
        abort(404)
    return render_template('users_list.html', users_list=users_list, amount=users_amount)


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


@auth_blueprint.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your account has been update!', category='success')
        return redirect(url_for('auth.account'))

    form.about_me.data = current_user.about_me
    form.username.data = current_user.username
    form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@auth_blueprint.route("/resetpasword", methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.new_password1.data).decode('utf-8')
        db.session.commit()
        flash('Password changed', category='success')
        return redirect(url_for('auth.account'))
    return render_template('reset password.html', form=form)


@auth_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_date = datetime.utcnow()
        db.session.commit()
