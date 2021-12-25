from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, DataRequired, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from .models import User
from .. import bcrypt


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('A username is required'),
                                                   Length(min=4, max=25, message='Name must have greater 4 '
                                                                                 'symbol and least 25 symbol'),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Username must have only letters, numbers, '
                                                          'dots or underscores')])
    email = StringField('Email', validators=[InputRequired('Email is required'),
                                             Regexp('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
                                                    message='Invalid Email')])
    password = PasswordField('Password', validators=[InputRequired('Password is required'),
                                                     Length(min=6, message='Must be at least 6')])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired('Password is required'),
                                                                     Length(min=6, message='Must be at least 6'),
                                                                     EqualTo('password')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Regexp('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('')


class UpdateAccountForm(FlaskForm):
    username = StringField('', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('', validators=[InputRequired('Email is required'),
                                             Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                                                    message='Invali Email')])
    picture = FileField('', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('')

    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already registered')


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])

    new_password1 = PasswordField('Password', validators=[InputRequired('Password is required'),
                                                          Length(min=6, message='Must be at least 6')])

    new_password2 = PasswordField('Repeat the password', validators=[InputRequired('Password is required'),
                                                                     Length(min=6, message='Must be at least 6'),
                                                                     EqualTo('new_password1')])

    def validate_old_password(self, field):
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('Error')
