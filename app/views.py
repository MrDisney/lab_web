from flask import Flask, render_template, request, flash
import os, sys, platform
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdAWdfz21zasdasdaw64!'

@app.route("/blog")
def blog():
    news_dict = {
        'Lab1': 'здано',
        'Lab2': 'здано',
        'Lab3': 'здано',
    }
    return render_template("blog.html", news_dict=news_dict, sys_info=request.headers.get('User-Agent'),
                           sys=sys.version, os_name=os.name, platform=platform.system(), release=platform.release(),
                           date=datetime.now())


@app.route("/news")
def sale():
    sale_dict = {
        'Це моя ': 'домашня сторінка'


    }
    return render_template("sale.html", sale_dict=sale_dict, sys_info=request.headers.get('User-Agent'),
                           sys=sys.version, os_name=os.name, platform=platform.system(), release=platform.release(),
                           date=datetime.now())


@app.route("/")
def aboutme():
    return render_template("aboutme.html", boolean=False, name='Іван', error='Wrong data',
                           sys_info=request.headers.get('User-Agent'), sys=sys.version, os_name=os.name,
                           platform=platform.system(), release=platform.release(), date=datetime.now())


# Lab 4
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required'),
                                                   Length(min=5, max=10, message='Must be at least 5 and at most 10 '
                                                                                 'characters')])
    password = PasswordField('password',
                             validators=[InputRequired('Password is required'), AnyOf(values=['password', 'secret'])])


@app.route("/form", methods=['GET', 'POST'])
def form():
    form = LoginForm()
    flash('Пароль повинен бути скритий')
    if form.validate_on_submit():
        return f'The username is {form.username.data}. The password is {form.password.data}'

    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
