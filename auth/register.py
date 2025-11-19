import uuid
from flask import render_template, request
from . import auth_bp
from extensions import db, bcrypt
from models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")  # or return "Register page"

<<<<<<< HEAD
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    if password != confirm:
=======
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    user_type = request.form.get("user_type")

    if not email or not password or not confirm_password or not user_type:
        return "Error: all fields are required"

    if not (
        email.endswith("@student.mmu.edu.my")
        or email.endswith("@mmu.edu.my")
    ):
        return "Error: email must be an MMU address"

    if password != confirm_password:
>>>>>>> b45f8209d4b7392c662abcedc5fd44dc57afe4ee
        return "Error: passwords do not match"

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(email=email, password_hash=pw_hash)

    db.session.add(user)
    db.session.commit()

<<<<<<< HEAD
    return "Registered"
=======
    # For now: show verification link directly (no real email sending yet)
    return f"Account created. Please verify using this link: /verify/{token}"

    
>>>>>>> b45f8209d4b7392c662abcedc5fd44dc57afe4ee
