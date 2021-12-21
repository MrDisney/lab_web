from flask import render_template, flash, redirect, url_for, abort
from flask_login import login_user, current_user, logout_user, login_required

from .models import User
from .. import db
from . import auth_blueprint
from .forms import SignUpForm, LoginForm


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


@auth_blueprint.route("/account")
@login_required
def account():
    return render_template('account.html')
