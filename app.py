import json
import re
import random
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Email is required'),
                                              Regexp('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'),
                                              Length(min=5, max=30, message='Email must be correct')])
    password1 = PasswordField('Password', validators=[InputRequired('Password is required'),
                                                       Length(min=6, message='Must be at least 6')])
    password2 = PasswordField('Confirm password', validators=[InputRequired('Password is required'),
                                                               Length(min=6, message='Passwords must be the same')])
    number = StringField('Number', validators=[InputRequired('Number is required'),
                                                Length(min=7, max=7, message='The length must be exactly 7')])
    pin = StringField('PIN code', validators=[InputRequired('Pin code is required'),
                                               Regexp('[0-9]{4}', message='Must be 4 digits of the PIN code'),
                                               Length(min=4, max=4)])
    year = SelectField('Year', choices=[2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
    serial = StringField('Serial number')
    doc_number = StringField('Document number')


@app.route("/", methods=['GET', 'POST'])
def form():
    form = LoginForm()


    if form.validate_on_submit():
        if form.password1.data == form.password2.data:
            regex = r'^[A-Z]{2}$' if int(form.year.data) < 2015 else r'^[A-Z][0-9]{2}$'
            length = 8 if int(form.year.data) < 2015 else 6
            serial_length = 2 if int(form.year.data) < 2015 else 3

            if not bool(re.search(regex, form.serial.data)) and len(form.serial.data) != serial_length:
                print(123)
                return render_template('index.html', form=form,
                                       s_error_message='before 2015 - 2 letters (for example, AB),'
                                                       'later - 1 letter and 2 numbers '
                                                       '(for example, C17, B20)')
            if len(form.doc_number.data) != length:
                return render_template('index.html', form=form, d_error_message='Before 2015 - 8 digits, '
                                                                                'later - 6 digits')

            data = {random.random(): {
                'email': form.email.data,
                'password': form.password1.data,
                'number': form.number.data,
                'pin': form.pin.data,
                'year': form.year.data,
                'serial': form.serial.data,
                'doc_number': form.doc_number.data,
            }, }

        try:
            with open('data.json', 'r') as file:
                file_data = json.load(file)
                file_data.update(data)

            with open('data.json', 'w', encoding='utf-8') as w_file:
                json.dump(file_data, w_file, ensure_ascii=False, indent=4)

        except FileNotFoundError and json.decoder.JSONDecodeError:
            with open('data.json', 'w', encoding='utf-8') as w_file:
                json.dump(data, w_file, ensure_ascii=False, indent=4)

        return f'<h1 style="text-align: center">Entered data sent to JSON file!</h1>'

    else:
        return render_template('index.html', form=form, error='Passwords are different')

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
