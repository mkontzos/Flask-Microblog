from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User

class QuestionForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(max=90)])
    body = TextAreaField (_l('Body of your question'), validators=[DataRequired(), Length(max=600)])
    category = SelectField(u'Categories', coerce=int)
    #category = SelectField(u'Categories', categories=['technology','programming','devops','statistics' ])
    submit = SubmitField(_l('Submit'))

class CategoryForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(max=30)])
    submit = SubmitField(_l('Submit'))

class AnswerForm(FlaskForm):
    body = StringField(_l('Answer body'), validators=[DataRequired(), Length(max=400)])
    submit = SubmitField(_l('Submit'))

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')