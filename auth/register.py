import uuid
from flask import render_template, request
from . import auth_bp
from extensions import db, bcrypt
from models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

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
        return "Error: passwords do not match"

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return "Error: email already registered"

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    token = str(uuid.uuid4())

    new_user = User(
        email=email,
        password_hash=hashed_pw,
        user_type=user_type,
        is_verified=False,
        verification_token=token,
    )

    db.session.add(new_user)
    db.session.commit()

    # For now: show verification link directly (no real email sending yet)
    return f"Account created. Please verify using this link: /verify/{token}"

    