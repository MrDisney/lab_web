from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, IntegerField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class CreateSubjectForm(FlaskForm):
    name_subject = StringField('Name Subject', validators=[InputRequired(), Length(min=1, max=30)])
    teacher = StringField('Teacher', validators=[InputRequired(), Length(min=1, max=30)])
    specialty = StringField('Specialty', validators=[InputRequired(), Length(min=1, max=50)])
    semester = IntegerField('Semester')
    type_occupation = SelectField('Type Occupation', choices=[('Lecture', 'Lecture'), ('Practical', 'Practical'),
                                                              ('Laboratory', 'Laboratory'), ('Seminar', 'Seminar')])

    control = SelectField('Type control', choices=[('Missing', 'Missing'), ('Test', 'Test'),
                                                   ('Examination', 'Examination')])

    submit = SubmitField('')
