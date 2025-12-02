from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Review, User, Reply, Report
from datetime import datetime
from sqlalchemy import func

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
    rating_responsiveness = int(request.form.get('rating_responsiveness', 0))
    rating_fairness = int(request.form.get('rating_fairness', 0))
    subject_id = request.form.get('subject_id')
    
    if not review_text or not all([rating_clarity, rating_engagement, rating_punctuality, rating_responsiveness, rating_fairness]):
        flash("Please fill all fields", "error")
        return redirect(url_for('reviews.create_review', lecturer_id=lecturer_id))
    
    review = Review(
        review_text=review_text,
        rating_clarity=rating_clarity,
        rating_engagement=rating_engagement,
        rating_punctuality=rating_punctuality,
        rating_responsiveness=rating_responsiveness,
        rating_fairness=rating_fairness,
        user_id=current_user.id,
        lecturer_id=lecturer_id,
        subject_id=subject_id if subject_id else None
    )
    
    db.session.add(review)
    db.session.commit()
    
    flash("Review submitted successfully!", "success")
    return redirect(url_for('reviews.lecturer_profile', lecturer_id=lecturer_id))

@reviews_bp.route('/lecturer/<int:lecturer_id>')
@login_required
def lecturer_profile(lecturer_id):
    lecturer = User.query.get_or_404(lecturer_id)
    if lecturer.user_type != 'lecturer':
        flash("Invalid lecturer", "error")
        return redirect(url_for('index'))
    
    reviews = Review.query.filter_by(lecturer_id=lecturer_id).all()
    
    if reviews:
        avg_clarity = db.session.query(func.avg(Review.rating_clarity)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_engagement = db.session.query(func.avg(Review.rating_engagement)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_punctuality = db.session.query(func.avg(Review.rating_punctuality)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_responsiveness = db.session.query(func.avg(Review.rating_responsiveness)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_fairness = db.session.query(func.avg(Review.rating_fairness)).filter_by(lecturer_id=lecturer_id).scalar()
        
        averages = {
            'clarity': round(avg_clarity, 1) if avg_clarity else 0,
            'engagement': round(avg_engagement, 1) if avg_engagement else 0,
            'punctuality': round(avg_punctuality, 1) if avg_punctuality else 0,
            'responsiveness': round(avg_responsiveness, 1) if avg_responsiveness else 0,
            'fairness': round(avg_fairness, 1) if avg_fairness else 0,
        }
    else:
        averages = None
    
    return render_template('lecturer_profile.html', lecturer=lecturer, reviews=reviews, averages=averages)

@reviews_bp.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.author != current_user:
        flash("You can only edit your own reviews", "error")
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('edit_review.html', review=review)
    
    review_text = request.form.get('review_text', '').strip()
    rating_clarity = int(request.form.get('rating_clarity', 0))
    rating_engagement = int(request.form.get('rating_engagement', 0))
    rating_punctuality = int(request.form.get('rating_punctuality', 0))
    rating_responsiveness = int(request.form.get('rating_responsiveness', 0))
    rating_fairness = int(request.form.get('rating_fairness', 0))
    
    if not review_text or not all([rating_clarity, rating_engagement, rating_punctuality, rating_responsiveness, rating_fairness]):
        flash("Please fill all fields", "error")
        return redirect(url_for('reviews.edit_review', review_id=review_id))
    
    review.review_text = review_text
    review.rating_clarity = rating_clarity
    review.rating_engagement = rating_engagement
    review.rating_punctuality = rating_punctuality
    review.rating_responsiveness = rating_responsiveness
    review.rating_fairness = rating_fairness
    
    db.session.commit()
    
    flash("Review updated successfully!", "success")
    return redirect(url_for('reviews.lecturer_profile', lecturer_id=review.lecturer_id))

@reviews_bp.route('/review/<int:review_id>/delete', methods=['GET'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.author != current_user:
        flash("You can only delete your own reviews", "error")
        return redirect(url_for('index'))

    lecturer_id = review.lecturer_id
    
    db.session.delete(review)
    db.session.commit()
    
    flash("Review deleted successfully!", "success")
    return redirect(url_for('reviews.lecturer_profile', lecturer_id=lecturer_id))

@reviews_bp.route('/review/<int:review_id>/reply', methods=['POST'])
@login_required
def add_reply(review_id):
    review = Review.query.get_or_404(review_id)
    
    if current_user.user_type not in ['student', 'lecturer']:
        flash("Only students and lecturers can reply", "error")
        return redirect(url_for('reviews.lecturer_profile', lecturer_id=review.lecturer_id))
    
    reply_text = request.form.get('reply_text', '').strip()
    
    if not reply_text:
        flash("Reply cannot be empty", "error")
        return redirect(url_for('reviews.lecturer_profile', lecturer_id=review.lecturer_id))
    
    reply = Reply(
        reply_text=reply_text,
        user_id=current_user.id,
        review_id=review_id
    )
    
    db.session.add(reply)
    db.session.commit()
    
    flash("Reply posted successfully!", "success")
    return redirect(url_for('reviews.lecturer_profile', lecturer_id=review.lecturer_id))

@reviews_bp.route('/review/<int:review_id>/report', methods=['POST'])
@login_required
def report_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    if current_user.user_type != 'student':
        flash("Only students can report reviews", "error")
        return redirect(url_for('reviews.lecturer_profile', lecturer_id=review.lecturer_id))
    
    existing_report = Report.query.filter_by(review_id=review_id, reporter_id=current_user.id).first()
    if existing_report:
        flash("You have already reported this review", "error")
        return redirect(url_for('reviews.lecturer_profile', lecturer_id=review.lecturer_id))
    
    reason = request.form.get('reason', '').strip()
    
    if not reason:
        flash("Please provide a reason for reporting", "error")
        return redirect(url_for('reviews.lecturer_profile', lecturer_id=review.lecturer_id))
    
    report = Report(
        review_id=review_id,
        reporter_id=current_user.id,
        reason=reason
    )
    
    db.session.add(report)
    db.session.commit()
    
    flash("Review reported successfully. Admins will review it.", "success")
    return redirect(url_for('reviews.lecturer_profile', lecturer_id=review.lecturer_id))

@reviews_bp.route('/analytics/<int:lecturer_id>')
@login_required
def analytics(lecturer_id):
    lecturer = User.query.get_or_404(lecturer_id)
    
    if current_user.id != lecturer_id and current_user.user_type != 'admin':
        flash("You don't have permission to view this analytics page", "error")
        return redirect(url_for('index'))
    
    if lecturer.user_type != 'lecturer':
        flash("Invalid lecturer", "error")
        return redirect(url_for('index'))
    
    reviews = Review.query.filter_by(lecturer_id=lecturer_id).all()
    total_reviews = len(reviews)
    
    if reviews:
        avg_clarity = db.session.query(func.avg(Review.rating_clarity)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_engagement = db.session.query(func.avg(Review.rating_engagement)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_punctuality = db.session.query(func.avg(Review.rating_punctuality)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_responsiveness = db.session.query(func.avg(Review.rating_responsiveness)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_fairness = db.session.query(func.avg(Review.rating_fairness)).filter_by(lecturer_id=lecturer_id).scalar()
        
        averages = {
            'clarity': round(avg_clarity, 1) if avg_clarity else 0,
            'engagement': round(avg_engagement, 1) if avg_engagement else 0,
            'punctuality': round(avg_punctuality, 1) if avg_punctuality else 0,
            'responsiveness': round(avg_responsiveness, 1) if avg_responsiveness else 0,
            'fairness': round(avg_fairness, 1) if avg_fairness else 0,
        }
        
        overall_rating = round((averages['clarity'] + averages['engagement'] + averages['punctuality'] + averages['responsiveness'] + averages['fairness']) / 5, 1)
        
        strongest = max(averages, key=averages.get)
        weakest = min(averages, key=averages.get)
    else:
        averages = None
        overall_rating = 0
        strongest = None
        weakest = None
    
    if current_user.user_type == 'admin':
        all_lecturers = User.query.filter_by(user_type='lecturer').all()
        lecturer_stats = []
        
        for lect in all_lecturers:
            lect_reviews = Review.query.filter_by(lecturer_id=lect.id).all()
            if lect_reviews:
                lect_avg_clarity = db.session.query(func.avg(Review.rating_clarity)).filter_by(lecturer_id=lect.id).scalar()
                lect_avg_engagement = db.session.query(func.avg(Review.rating_engagement)).filter_by(lecturer_id=lect.id).scalar()
                lect_avg_punctuality = db.session.query(func.avg(Review.rating_punctuality)).filter_by(lecturer_id=lect.id).scalar()
                lect_avg_responsiveness = db.session.query(func.avg(Review.rating_responsiveness)).filter_by(lecturer_id=lect.id).scalar()
                lect_avg_fairness = db.session.query(func.avg(Review.rating_fairness)).filter_by(lecturer_id=lect.id).scalar()
                
                lect_overall = round((lect_avg_clarity + lect_avg_engagement + lect_avg_punctuality + lect_avg_responsiveness + lect_avg_fairness) / 5, 1)
                
                lecturer_stats.append({
                    'email': lect.email,
                    'id': lect.id,
                    'overall': lect_overall,
                    'total_reviews': len(lect_reviews)
                })
        
        lecturer_stats.sort(key=lambda x: x['overall'], reverse=True)
    else:
        lecturer_stats = None
    
    return render_template('analytics.html', 
                         lecturer=lecturer, 
                         total_reviews=total_reviews, 
                         averages=averages,
                         overall_rating=overall_rating,
                         strongest=strongest,
                         weakest=weakest,
                         lecturer_stats=lecturer_stats)

@reviews_bp.route('/student-analytics/<int:lecturer_id>')
@login_required
def student_analytics(lecturer_id):
    lecturer = User.query.get_or_404(lecturer_id)
    
    if lecturer.user_type != 'lecturer':
        flash("Invalid lecturer", "error")
        return redirect(url_for('index'))
    
    reviews = Review.query.filter_by(lecturer_id=lecturer_id).all()
    total_reviews = len(reviews)
    
    if reviews:
        avg_clarity = db.session.query(func.avg(Review.rating_clarity)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_engagement = db.session.query(func.avg(Review.rating_engagement)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_punctuality = db.session.query(func.avg(Review.rating_punctuality)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_responsiveness = db.session.query(func.avg(Review.rating_responsiveness)).filter_by(lecturer_id=lecturer_id).scalar()
        avg_fairness = db.session.query(func.avg(Review.rating_fairness)).filter_by(lecturer_id=lecturer_id).scalar()
        
        averages = {
            'clarity': round(avg_clarity, 1) if avg_clarity else 0,
            'engagement': round(avg_engagement, 1) if avg_engagement else 0,
            'punctuality': round(avg_punctuality, 1) if avg_punctuality else 0,
            'responsiveness': round(avg_responsiveness, 1) if avg_responsiveness else 0,
            'fairness': round(avg_fairness, 1) if avg_fairness else 0,
        }
        
        overall_rating = round((averages['clarity'] + averages['engagement'] + averages['punctuality'] + averages['responsiveness'] + averages['fairness']) / 5, 1)
    else:
        averages = None
        overall_rating = 0
    
    user_review = None
    if current_user.user_type == 'student':
        user_review = Review.query.filter_by(user_id=current_user.id, lecturer_id=lecturer_id).first()
    
    distribution = None
    if reviews:
        distribution = {
            'clarity': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'engagement': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'punctuality': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'responsiveness': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'fairness': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
        }
        
        for review in reviews:
            distribution['clarity'][review.rating_clarity] += 1
            distribution['engagement'][review.rating_engagement] += 1
            distribution['punctuality'][review.rating_punctuality] += 1
            distribution['responsiveness'][review.rating_responsiveness] += 1
            distribution['fairness'][review.rating_fairness] += 1
    
    all_lecturers_avg = None
    comparison_text = None
    if reviews:
        all_lecturers = User.query.filter_by(user_type='lecturer').all()
        all_ratings = []
        
        for lect in all_lecturers:
            lect_reviews = Review.query.filter_by(lecturer_id=lect.id).all()
            if lect_reviews:
                lect_avg_clarity = db.session.query(func.avg(Review.rating_clarity)).filter_by(lecturer_id=lect.id).scalar()
                lect_avg_engagement = db.session.query(func.avg(Review.rating_engagement)).filter_by(lecturer_id=lect.id).scalar()
                lect_avg_punctuality = db.session.query(func.avg(Review.rating_punctuality)).filter_by(lecturer_id=lect.id).scalar()
                lect_avg_responsiveness = db.session.query(func.avg(Review.rating_responsiveness)).filter_by(lecturer_id=lect.id).scalar()
                lect_avg_fairness = db.session.query(func.avg(Review.rating_fairness)).filter_by(lecturer_id=lect.id).scalar()
                
                lect_overall = (lect_avg_clarity + lect_avg_engagement + lect_avg_punctuality + lect_avg_responsiveness + lect_avg_fairness) / 5
                all_ratings.append(lect_overall)
        
        if all_ratings:
            all_lecturers_avg = round(sum(all_ratings) / len(all_ratings), 1)
            difference = round(overall_rating - all_lecturers_avg, 1)
            
            if difference >= 0.1:
                comparison_text = f"ABOVE AVERAGE (+{difference} points)"
            elif difference <= -0.1:
                comparison_text = f"BELOW AVERAGE ({difference} points)"
            else:
                comparison_text = "AT AVERAGE"
    
    return render_template('student_analytics.html', 
                         lecturer=lecturer, 
                         total_reviews=total_reviews, 
                         averages=averages,
                         overall_rating=overall_rating,
                         user_review=user_review,
                         distribution=distribution,
                         all_lecturers_avg=all_lecturers_avg,
                         comparison_text=comparison_text)