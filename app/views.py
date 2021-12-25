import json

from flask import render_template, session, flash, redirect, url_for, abort

from . import app, db
from .controller import user_info, validate_fields, json_data
from .forms import Form, DocRegistration, SignUpForm, LoginForm
from .models import User


@app.route("/")
def index():
    return render_template("index.html", user_info=user_info())


@app.route("/about")
def about():
    info = "Павлишин Іван студент групи ІПЗ-31"
    checker = True
    return render_template("about.html", checker=checker, info=info, user_info=user_info())


@app.route("/projects")
def projects():
    projects_list = ['Lab1', 'Lab2', 'Lab3', 'Lab4', 'Lab5', 'Lab6']
    return render_template("projects.html", projects_list=projects_list, user_info=user_info())


@app.route("/contacts")
def contacts():
    contact_dict = {
        'Номер телефону': '380956398000',
        'Електронна пошта': 'email@gmail.com',
        'Телеграм': '@paveldurov'
    }
    return render_template("contacts.html", contacts_dict=contact_dict, user_info=user_info())


@app.route("/form", methods=['GET', 'POST'])
def form():
    form = Form()

    flash('Пароль повинен бути сикретним')
    if form.validate_on_submit():
        return f'<h1>The username is {form.username.data}. The password is {form.password.data}</h1>'
    return render_template('form.html', form=form, user_info=user_info())


@app.route("/doc_registration", methods=['GET', 'POST'])
def doc_registration():
    doc_reg = DocRegistration()
    validate_fields(doc_reg)

    if doc_reg.validate_on_submit():
        session['email'] = doc_reg.email.data
        json_data(doc_reg)
        # flash('Data successfully added to json')
        return redirect(url_for('doc_registration'))

    try:
        session_data = session['email']
    except KeyError:
        return render_template('doc_registration.html', doc_reg=doc_reg)

    with open('data.json') as file:
        data = json.load(file)

    return render_template('doc_registration.html', doc_reg=doc_reg, email=session_data,
                           number=data[session_data]['number'], pin=data[session_data]['pin'],
                           year=data[session_data]['year'], serial=data[session_data]['serial'],
                           doc_number=data[session_data]['doc_number'])


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    registration = SignUpForm()
    if registration.validate_on_submit():
        user = User(username=registration.username.data, email=registration.email.data,
                    password=registration.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {registration.username.data} !', category='success')
        return redirect(url_for('login'))
    return render_template('signup.html', registration=registration)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.verify_password(login_form.password.data):
            flash(f'You have been logged by email {user.email}!', category='success')
            return redirect(url_for('login'))
        else:
            flash('Invalid login or password!', category='warning')
            return redirect(url_for('login'))

    return render_template('login.html', login_form=login_form)


@app.route("/users", methods=['GET', 'POST'])
def users():
    users_list = User.query.all()
    users_amount = User.query.count()
    if users_amount == 0:
        abort(404)
    return render_template('users_list.html', users_list=users_list, amount=users_amount)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html')
