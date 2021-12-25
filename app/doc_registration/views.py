import json

from flask import render_template, flash, session, redirect, url_for

from . import doc_registration_blueprint
from .forms import Form, DocRegistration
from ..controller import validate_fields, json_data, user_info


@doc_registration_blueprint.route("/form", methods=['GET', 'POST'])
def form():
    form = Form()
    flash('Пароль повинен бути сикретним')
    if form.validate_on_submit():
        return f'<h1>The username is {form.username.data}. The password is {form.password.data}</h1>'
    return render_template('form.html', form=form, user_info=user_info())


@doc_registration_blueprint.route("/doc_registration", methods=['GET', 'POST'])
def doc_registration():
    doc_reg = DocRegistration()
    validate_fields(doc_reg)

    if doc_reg.validate_on_submit():
        session['email'] = doc_reg.email.data
        json_data(doc_reg)
        flash('Data successfully added to json')
        return redirect(url_for('doc_registration.doc_registration'))

    try:
        session_data = session['email']
        with open('data.json') as file:
            data = json.load(file)

        return render_template('doc_registration.html', doc_reg=doc_reg, email=session_data,
                               number=data[session_data]['number'], pin=data[session_data]['pin'],
                               year=data[session_data]['year'], serial=data[session_data]['serial'],
                               doc_number=data[session_data]['doc_number'])
    except KeyError:
        return render_template('doc_registration.html', doc_reg=doc_reg)
