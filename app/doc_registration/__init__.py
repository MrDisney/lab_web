from flask import Blueprint

doc_registration_blueprint = Blueprint('doc_registration', __name__, template_folder="templates")

from . import views
