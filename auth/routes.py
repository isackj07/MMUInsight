from flask import render_template, redirect, url_for, flash
from . import auth_bp
from auth.decorators import login_required, admin_required
from models import User, Report, Review
from extensions import db

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return "Student dashboard (placeholder - requires login)"

@auth_bp.route("/admin")
@admin_required
def admin_dashboard():
    users = User.query.all()
    total_users = len(users)
    verified_users = sum(1 for u in users if u.is_verified)
    admin_count = sum(1 for u in users if u.user_type == "admin")
    
    pending_reports = Report.query.filter_by(status='pending').count()

    return render_template(
        "admin_dashboard.html",
        users=users,             
        total_users=total_users,
        verified_users=verified_users,
        admin_count=admin_count,
        pending_reports=pending_reports,
    )

@auth_bp.route("/admin/users")
@admin_required
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)

@auth_bp.route("/admin/user/<int:user_id>/verify")
@admin_required
def admin_verify_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_verified = True
        db.session.commit()
    return redirect(url_for("auth.admin_users"))

@auth_bp.route("/admin/user/<int:user_id>/make-admin")
@admin_required
def admin_make_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.user_type = "admin"
        db.session.commit()
    return redirect(url_for("auth.admin_users"))

@auth_bp.route("/admin/user/<int:user_id>/remove-admin")
@admin_required
def admin_remove_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.user_type = "student"  
        db.session.commit()
    return redirect(url_for("auth.admin_users"))

@auth_bp.route("/admin/user/<int:user_id>/suspend")
@admin_required
def admin_suspend_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_verified = False    
        db.session.commit()
    return redirect(url_for("auth.admin_users"))

@auth_bp.route("/admin/user/<int:user_id>/delete")
@admin_required
def admin_delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("auth.admin_users"))

@auth_bp.route("/admin/reports")
@admin_required
def admin_reports():
    reports = Report.query.order_by(Report.report_date.desc()).all()
    return render_template("admin_reports.html", reports=reports)

@auth_bp.route("/admin/report/<int:report_id>/dismiss")
@admin_required
def admin_dismiss_report(report_id):
    report = Report.query.get(report_id)
    if report:
        report.status = 'dismissed'
        db.session.commit()
        flash("Report dismissed", "success")
    return redirect(url_for("auth.admin_reports"))

@auth_bp.route("/admin/report/<int:report_id>/delete-review")
@admin_required
def admin_delete_reported_review(report_id):
    report = Report.query.get(report_id)
    if report:
        review = report.review
        db.session.delete(review)
        db.session.commit()
        flash("Review deleted", "success")
    return redirect(url_for("auth.admin_reports"))