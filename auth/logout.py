from flask import session
from . import auth_bp

@auth_bp.route("/logout")
def logout():
    session.clear()
    return "Logged out"
