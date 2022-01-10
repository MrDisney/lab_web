from flask import Flask, g, request, jsonify
from functools import wraps
from ..subjects.models import Subject
from .. import db

from . import api_exz_blueprint

api_username = 'admin'
api_password = 'password'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403

    return decorated


@api_exz_blueprint.route('/subjects', methods=['GET'])
@protected
def get_subjects():
    subjects = Subject.query.all()
    return_values = [{"id": subject.id,
                      "name_subject": subject.name_subject,
                      "teacher": subject.teacher,
                      "specialty": subject.specialty,
                      "semester": subject.semester,
                      "control": subject.control.value,
                      "type_occupation": subject.type_occupation.value} for subject in subjects]

    return jsonify({'Subjects': return_values})


@api_exz_blueprint.route('/subject/<int:id>', methods=['GET'])
@protected
def get_subject(id):
    subject = Subject.query.get_or_404(id)
    return jsonify({"id": subject.id,
                    "name_subject": subject.name_subject,
                    "teacher": subject.teacher,
                    "specialty": subject.specialty,
                    "semester": subject.semester,
                    "control": subject.control.value,
                    "type_occupation": subject.type_occupation.value})


@api_exz_blueprint.route('/subject', methods=['POST'])
def add_subject():
    new_sub_data = request.get_json()

    sub = Subject(
        name_subject=new_sub_data['name_subject'],
        teacher=new_sub_data['teacher'],
        specialty=new_sub_data['specialty'],
        semester=new_sub_data['semester'],
        type_occupation=new_sub_data['type_occupation'],
        control=new_sub_data['control'],
    )

    db.session.add(sub)
    db.session.commit()
    return jsonify({"id": sub.id,
                    "name_subject": sub.name_subject,
                    "teacher": sub.teacher,
                    "specialty": sub.specialty,
                    "semester": sub.semester,
                    "control": sub.control.value,
                    "type_occupation": sub.type_occupation.value})


@api_exz_blueprint.route('/subject/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit_subject(id):
    subject = Subject.query.get(id)
    if not subject:
        return jsonify({"Message": "Subject does not exist"})

    update_subject_data = request.get_json()

    subject.name_subject = update_subject_data['name_subject']
    subject.teacher = update_subject_data['teacher']
    subject.specialty = update_subject_data['specialty']
    subject.semester = update_subject_data['semester']
    subject.type_occupation = update_subject_data['type_occupation']
    subject.control = update_subject_data['control']

    db.session.add(subject)
    db.session.commit()

    return jsonify({"id": subject.id,
                    "name_subject": subject.name_subject,
                    "teacher": subject.teacher,
                    "specialty": subject.specialty,
                    "semester": subject.semester,
                    "control": subject.control.value,
                    "type_occupation": subject.type_occupation.value})


@api_exz_blueprint.route('/subject/<int:id>', methods=['DELETE'])
@protected
def delete_institution(id):
    sub = Subject.query.get_or_404(id)
    db.session.delete(sub)
    db.session.commit()

    return jsonify({'Message': 'The subject has been deleted!'})
