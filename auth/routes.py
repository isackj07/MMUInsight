from auth import auth_bp
from auth.decorators import login_required, admin_required

@auth_bp.route("/")
def index():
    return "MMUInsight home (placeholder)"

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return "Student dashboard (placeholder - requires login)"

@auth_bp.route("/admin-only")
@admin_required
def admin_only():
    return "Admin-only area (requires user_type = 'admin')"

