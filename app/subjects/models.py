from .. import db
import enum


class SubjectType(enum.Enum):
    Lecture = 'Lecture'
    Practical = 'Practical'
    Laboratory = 'Laboratory'
    Seminar = 'Seminar'


class ControlType(enum.Enum):
    Missing = 'Missing'
    Test = 'Test'
    Examination = 'Examination'


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_subject = db.Column(db.String(30), nullable=False)
    teacher = db.Column(db.String(30), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    type_occupation = db.Column(db.Enum(SubjectType))
    control = db.Column(db.Enum(ControlType))
