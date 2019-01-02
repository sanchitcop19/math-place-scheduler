from flask_wtf import FlaskForm
from wtforms import widgets, BooleanField, SubmitField

class DropForm(FlaskForm):
    drop = BooleanField()
    submit = SubmitField('Drop Shifts')