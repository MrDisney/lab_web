import os, platform, sys, datetime
from flask import Flask, render_template, request

app = Flask(__name__)


def user_info():
    info_dict = {
        'system': f'{platform.system()} {platform.release()} {os.name}',
        'user_agent': request.headers.get('User-Agent'),
        'python': sys.version
    }
    return info_dict


@app.route("/")
def index():
    return render_template("index.html", user_info=user_info())


@app.route("/about")
def about():
    info = "I'm write my first Flask app!"
    checker = True
    return render_template("about.html", checker=checker, info=info, user_info=user_info())


@app.route("/projects")
def projects():
    projects_list = ['project1', 'project2', 'project3', 'project4', 'project5', 'project6', 'project7']
    return render_template("projects.html", projects_list=projects_list, user_info=user_info())


@app.route("/contacts")
def contacts():
    contact_dict = {
        'Cell': '123456789',
        'Email': 'email@gmail.com',
        'Telegram': '@nickname'
    }
    return render_template("contacts.html", contacts_dict=contact_dict, user_info=user_info())


if __name__ == '__main__':
    app.run(debug=True)