from flask import redirect, url_for
from extensions import db
from models import User
from . import auth_bp


@auth_bp.route("/verify/<token>")
def verify(token):
    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return "Error: invalid or expired verification link"

    if user.is_verified:
        return "Your account is already verified. You can log in."

    user.is_verified = True
    user.verification_token = None
    db.session.commit()

    return "Your account has been verified. You can now log in."

  
