import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'secret_key'
WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
