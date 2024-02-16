from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField


class AddPetForm(FlaskForm):
    name = StringField("Pet Name")
    species = StringField("Species")
    photo_url = StringField("Photo URL")
    age = IntegerField("Age")
    notes = StringField("Notes")
    available = BooleanField("Available")


class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL")
    notes = StringField("Notes")
    available = BooleanField("Available")
