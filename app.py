from flask import Flask, flash, redirect, render_template, request, url_for

from forms import AddPetForm, EditPetForm
from models import Pet, connect_db, db

app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pet_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    pets = Pet.query.all()

    return render_template("adoption_page.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet_form():
    """
    Display and process the form for adding a new pet.

    Returns:
        If the form is successfully submitted, adds the new pet to the database
        and redirects to the home page. Otherwise, renders the add pet form template.
    """
    form = AddPetForm()

    if form.validate_on_submit():
        # Extract data from the form and create a new Pet object
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)

        # Add the new pet to the database and commit the transaction
        db.session.add(new_pet)
        db.session.commit()

        # Flash a message and redirect to the home page
        flash(f"{new_pet.name} added.")
        return redirect(url_for("home_page"))
    else:
        # Render the add pet form template
        return render_template("add_pet_form.html", form=form)


@app.route("/edit", methods=["GET", "POST"])
def edit_pet_form():
    """
    Display and process the form for editing a pet.

    Returns:
        If the form is successfully submitted, updates the pet in the database
        and redirects to the home page. Otherwise, renders the edit pet form template.
    """
    form = EditPetForm()

    if form.validate_on_submit():
        # Extract data from the form and update the pet in the database
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        pet = Pet.query.get(data["id"])
        pet.update(**data)

        # Commit the transaction
        db.session.commit()

        # Flash a message and redirect to the home page
        flash(f"{pet.name} updated.")
        return redirect(url_for("home_page"))
    else:
        # Render the edit pet form template
        return render_template("edit_pet_form.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
