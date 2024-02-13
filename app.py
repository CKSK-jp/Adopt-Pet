from flask import Flask, flash, redirect, render_template, request, url_for

from models import Post, PostTag, Tag, User, connect_db, db, default_img

app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users_db_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()
    
  
@app.route("/")
def home_page():
  render_template("adoption_page.html")