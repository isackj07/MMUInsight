import uuid
from flask import render_template, request
from extensions import db, bcrypt
from models import User
from . import auth_bp


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    if password != confirm:
        return "Error: passwords do not match"

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(email=email, password_hash=pw_hash)

    db.session.add(user)
    db.session.commit()

    return "Registered"
