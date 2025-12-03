from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def login_required(f):
    """Use flask_login.login_required instead of this - kept for compatibility"""
    from flask_login import login_required as flask_login_required
    return flask_login_required(f)

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != "admin":
            return redirect(url_for("index"))  
        return f(*args, **kwargs)
    return wrapper