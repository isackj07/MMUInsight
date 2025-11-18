from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from extensions import db, bcrypt
from models import User
from . import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Please fill all fields", "error")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        flash("Invalid email or password", "error")
        return redirect(url_for("auth.login"))

    if not user.is_verified:
        flash("Please verify your email first", "error")
        return redirect(url_for("auth.login"))

    login_user(user, remember=True)
    flash("Login successful!", "success")

    next_page = request.args.get("next")
    return redirect(next_page) if next_page else redirect(url_for("index"))

