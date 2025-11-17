from flask import Blueprint, render_template, request
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
