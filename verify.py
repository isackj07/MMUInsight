from flask import Blueprint
from app import db, User

verify_bp = Blueprint('verify_bp', __name__)

@verify_bp.route('/verify/<token>')
def verify_email(token):
    # look up user by token
    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return "Invalid or expired verification link"

    # mark them verified
    user.is_verified = True
    user.verification_token = None
    db.session.commit()

    return "Your account has been verified. You can now log in."