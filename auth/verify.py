from . import auth_bp
from extensions import db
from models import User

@auth_bp.route("/verify/<token>")
def verify(token):
    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return "Invalid or expired verification link"

    user.is_verified = True
    user.verification_token = None
    db.session.commit()

    return "Your account has been verified. You can now log in."
  
