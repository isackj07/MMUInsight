import uuid
from flask import render_template, request, redirect, url_for, flash
from . import auth_bp
from extensions import db, bcrypt
from models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    user_type = request.form.get("user_type", "student")

    if not email or not password or not confirm_password or not user_type:
        flash("All fields are required", "error")
        return redirect(url_for("auth.register"))

    if email.endswith("@student.mmu.edu.my"):
        user_type = "student"
    elif email.endswith("@mmu.edu.my"):
        user_type = "lecturer"
    else:
        return "Error: email must be an MMU address"

    if password != confirm_password:
        flash("Passwords do not match", "error")
        return redirect(url_for("auth.register"))

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    token = str(uuid.uuid4())

    user = User(
        email=email,
        password_hash=pw_hash,
        user_type=user_type,
        verification_token=token
    )

    db.session.add(user)
    db.session.commit()

    flash(f"Account created. Verify at: /verify/{token}", "success")
    return redirect(url_for("auth.login"))
