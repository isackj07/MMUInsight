from flask import render_template, redirect, url_for
from auth import auth_bp
from auth.decorators import login_required, admin_required
from models import User
from extensions import db

@auth_bp.route("/")
def index():
    return "MMUInsight home (placeholder)"

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return "Student dashboard (placeholder - requires login)"

@auth_bp.route("/admin")
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    verified_users = User.query.filter_by(is_verified=True).count()
    admin_count = User.query.filter_by(user_type="admin").count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        verified_users=verified_users,
        admin_count=admin_count,
    )


@auth_bp.route("/admin/users")
@admin_required
def admin_users():
    users = User.query.order_by(User.id).all()
    return render_template("admin_users.html", users=users)


@auth_bp.route("/admin/users/<int:user_id>/verify")
@admin_required
def admin_verify_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    return redirect(url_for("auth.admin_users"))


@auth_bp.route("/admin/users/<int:user_id>/make-admin")
@admin_required
def admin_make_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.user_type = "admin"
    db.session.commit()
    return redirect(url_for("auth.admin_users"))


@auth_bp.route("/admin/users/<int:user_id>/delete")
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("auth.admin_users"))



