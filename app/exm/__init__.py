from flask import Blueprint

api_exz_blueprint = Blueprint('exz', __name__, )

from . import views
