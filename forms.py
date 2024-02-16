from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import URL, AnyOf, NumberRange


class AddPetForm(FlaskForm):
    name = StringField("Pet Name")
    species = StringField("Species", validators=[AnyOf(["cat", "dog", "porcupine"])])
    photo_url = StringField(
        "Photo URL", validators=[URL(message="Must be a valid URL")]
    )
    age = IntegerField(
        "Age",
        validators=[NumberRange(min=0, max=30, message="Age must be between 0 and 30")],
    )
    notes = StringField("Notes")
    available = BooleanField("Available", default=True)


class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL")
    notes = StringField("Notes")
    available = BooleanField("Available")
