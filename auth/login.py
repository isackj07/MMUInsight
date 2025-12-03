from flask import render_template, request, redirect, url_for
from flask_login import login_user
from . import auth_bp
from extensions import bcrypt
from models import User

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember", False)

    user = User.query.filter_by(email=email).first()

    if not user:
        return "Error: invalid email or password"

    if not user.is_verified:
        return "Error: account not verified yet"

    if not bcrypt.check_password_hash(user.password_hash, password):
        return "Error: invalid email or password"

    login_user(user, remember=remember)

    return f"Login OK for {user.email}"

