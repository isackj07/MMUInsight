from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in first", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in first", "error")
            return redirect(url_for("auth.login"))
        if current_user.user_type != "admin":
            flash("Admin access required", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return wrapper