import uuid
from flask import render_template, request
from . import auth_bp
from extensions import db, bcrypt
from models import User


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")

    email = request.form.get("email")

    if not email:
        return "Please enter your email."

    user = User.query.filter_by(email=email).first()

    if not user:
        # For now just say this, no need to reveal if email exists
        return "If this email exists, a reset link has been generated."

    token = str(uuid.uuid4())
    user.reset_token = token
    db.session.commit()

    # Temporary: show link directly instead of sending email
    return f"Password reset link (temporary): /reset-password/{token}"


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if not user:
        return "Invalid or expired reset link."

    if request.method == "GET":
        return render_template("reset_password.html")

    new_pw = request.form.get("password")
    confirm_pw = request.form.get("confirm_password")

    if not new_pw or not confirm_pw:
        return "Please fill in both password fields."

    if new_pw != confirm_pw:
        return "Passwords do not match."

    user.password_hash = bcrypt.generate_password_hash(new_pw).decode("utf-8")
    user.reset_token = None
    db.session.commit()

    return "Password reset successfully. You can now log in."
