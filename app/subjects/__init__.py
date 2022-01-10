from flask import Blueprint

sub_blueprint = Blueprint('sub', __name__, template_folder="templates/subjects")

from . import views
