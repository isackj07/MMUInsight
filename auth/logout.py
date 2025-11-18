from flask import redirect, url_for, flash
from flask_login import logout_user, login_required
from . import auth_bp


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('auth.login'))
