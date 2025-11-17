from flask import Blueprint, render_template, request, redirect, url_for, session
from app import User, db, bcrypt

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    user_type = request.form.get("user_type")

    if not (email.endswith("@student.mmu.edu.my") or email.endswith("@mmu.edu.my")):
        return "Error: email must be an MMU address"

    if password != confirm_password:
        return "Error: passwords do not match"

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return "Error: email already registered"

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        email=email,
        password_hash=hashed_pw,   
        user_type=user_type,
        is_verified=False       
    )

    db.session.add(new_user)
    db.session.commit()

    return f"User registered: {email} as {user_type}"
    
@register_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return "Error: invalid email or password"

    try:
        if not user.is_verified:
            return "Error: account not verified yet"
    except AttributeError:
        pass

    if not bcrypt.check_password_hash(user.password_hash, password):
        return "Error: invalid email or password"

    session["user_id"] = user.id
    session["user_type"] = user.user_type

    return f"Login OK for {user.email}"

@register_bp.route('/logout')
def logout():
    session.clear()
    return "Logged out"    