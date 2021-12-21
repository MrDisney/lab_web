from flask import render_template

from flask import current_app as app
from .controller import user_info


@app.route("/index")
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
    projects_list = ['Lab1', 'Lab2', 'Lab3', 'lab4', 'Lab5', 'Lab6']
    return render_template("projects.html", projects_list=projects_list, user_info=user_info())


@app.route("/contacts")
def contacts():
    contact_dict = {
        'Номер телефону': '380956398000',
        'Електронна пошта': 'email@gmail.com',
        'Телеграм': '@paveldurov'
    }
    return render_template("contacts.html", contacts_dict=contact_dict, user_info=user_info())


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html')
