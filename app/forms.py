from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, AnyOf, Regexp, EqualTo, ValidationError, DataRequired

from .models import User


class Form(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required'),
                                                   Length(min=5, max=10,
                                                          message='Username length must be in range 5-10')])
    password = PasswordField('password', validators=[InputRequired('Password is required'),
                                                     AnyOf(values=['password', 'secret'])])


class DocRegistration(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Email is required'),
                                              Regexp('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'),
                                              Length(min=5, max=30, message='Email must be correct')])
    password = PasswordField('Password', validators=[InputRequired('Password is required'),
                                                      Length(min=6, message='Must be at least 6')])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired('Password is required'),
                                                                      Length(min=6,
                                                                             message='Passwords must be the same'),
                                                                      EqualTo('password')])
    number = StringField('Number', validators=[InputRequired('Number is required'),
                                                Length(min=7, max=7, message='The length must be exactly 7')])
    pin = StringField('PIN code', validators=[InputRequired('Pin code is required'),
                                               Regexp('[0-9]{4}', message='Must be 4 digits of the PIN code'),
                                               Length(min=4, max=4)])
    year = SelectField('Year', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
    serial = StringField('Serial number')
    doc_number = StringField('Document number')


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

