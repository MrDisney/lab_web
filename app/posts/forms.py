from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=60)])
    text = TextAreaField('Text', validators=[Length(max=500)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('type', choices=[('News', 'News'), ('Publication', 'Publication'), ('Other', 'Other')])
    category = SelectField(u'Category', coerce=int)
    enabled = BooleanField('Enabled', )
    submit = SubmitField('')


class CategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired(), Length(min=2, max=60)])
    submit = SubmitField('')
