from flask_wtf import FlaskForm
from wtforms import widgets, BooleanField, SubmitField

class DropForm(FlaskForm):
    submit = SubmitField('Drop Shifts')

class PickupForm(FlaskForm):
    submit = SubmitField("Pickup Shifts")

class AddForm(FlaskForm):
    submit = SubmitField("Add Shifts")
