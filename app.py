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
    Render the add pet form and handle form submission.
    If the form is submitted, add the new pet to the database.
    """
    form = AddPetForm()

    if request.method == "POST":
        if form.validate_on_submit() and "csrf_token" in form.data:
            new_pet_data = {
                key: value for key, value in form.data.items() if key != "csrf_token"
            }
            new_pet = Pet(**new_pet_data)
            db.session.add(new_pet)
            db.session.commit()
            flash(f"{new_pet.name} added.", category="success")
            return redirect(url_for("home_page"))
        else:
            flash(f"Error adding pet: {form.errors}", category="error")
            return render_template("add_pet_form.html", form=form)

    return render_template("add_pet_form.html", form=form)


@app.route("/display/<int:pet_id>")
def display_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template("display_pet.html", pet=pet)


@app.route("/edit/<int:pet_id>", methods=["GET", "POST"])
def edit_pet_form(pet_id):
    """
    Render the form for editing a pet's information and process the form submission.
    Args:
        pet_id (int): The ID of the pet to edit.
    Returns:
        rendered template: The form for editing a pet's information or a redirect after form submission.
    """
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(pet)
            db.session.commit()
            flash(f"{pet.name} updated.", category="success")
            return redirect(url_for("display_pet", pet_id=pet.id))
        else:
            flash(f"{pet.name} not updated.", category="error")
            return render_template("edit_pet_form.html", form=form)
    return render_template("edit_pet_form.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
