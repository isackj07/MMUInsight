from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Review, User

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/create_review/<int:lecturer_id>', methods=['GET', 'POST'])
@login_required
def create_review(lecturer_id):
    if current_user.user_type != 'student':
        flash("Only students can write reviews", "error")
        return redirect(url_for('index'))
    
    lecturer = User.query.get_or_404(lecturer_id)
    if lecturer.user_type != 'lecturer':
        flash("Invalid lecturer", "error")
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('create_review.html', lecturer=lecturer)
    
    review_text = request.form.get('review_text', '').strip()
    rating_clarity = int(request.form.get('rating_clarity', 0))
    rating_engagement = int(request.form.get('rating_engagement', 0))
    rating_punctuality = int(request.form.get('rating_punctuality', 0))
    rating_helpfulness = int(request.form.get('rating_helpfulness', 0))
    rating_workload = int(request.form.get('rating_workload', 0))
    subject_id = request.form.get('subject_id')
    
    if not review_text or not all([rating_clarity, rating_engagement, rating_punctuality, rating_helpfulness, rating_workload]):
        flash("Please fill all fields", "error")
        return redirect(url_for('reviews.create_review', lecturer_id=lecturer_id))
    
    review = Review(
        review_text=review_text,
        rating_clarity=rating_clarity,
        rating_engagement=rating_engagement,
        rating_punctuality=rating_punctuality,
        rating_helpfulness=rating_helpfulness,
        rating_workload=rating_workload,
        user_id=current_user.id,
        lecturer_id=lecturer_id,
        subject_id=subject_id if subject_id else None
    )
    
    db.session.add(review)
    db.session.commit()
    
    flash("Review submitted successfully!", "success")
    return redirect(url_for('index'))