from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from . import auth_bp
from extensions import bcrypt
from models import User

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Please fill all fields", "error")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Invalid email or password", "error")
        return redirect(url_for("auth.login"))

    if not user.is_verified:
        flash("Account not verified yet", "error")
        return redirect(url_for("auth.login"))

    if not bcrypt.check_password_hash(user.password_hash, password):
        flash("Invalid email or password", "error")
        return redirect(url_for("auth.login"))

    login_user(user, remember=True)
    flash("Login successful!", "success")
    return redirect(url_for('index'))

