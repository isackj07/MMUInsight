from flask import blueprint, request, render_template, redirect, url_for, flash
from app import db, user, review, subject  # import models from your app.py

# this is your blueprint
reviews_bp = blueprint('reviews', __name__)

# --- mock user system (for testing) ---
# test your code without a real login system.
# pretend a student (user id 1) is logged in.
class mockcurrentuser:
    def __init__(self, id, user_type):
        self.id = id
        self.user_type = user_type

current_user = mockcurrentuser(id=1, user_type='student') # simulate student login

def login_required(f):
    """mock login decorator."""
    return f

def student_only(f):
    """
    security check for deliverable 1.
    checks if the mock user is a 'student'.
    """
    def wrap(*args, **kwargs):
        if current_user.user_type != 'student':
            flash('only students can write reviews.', 'error')
            return redirect(url_for('main.index')) # assumes you have a 'main.index' route
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap
# --- end of mock system ---


@reviews_bp.route('/create_review/<int:lecturer_id>', methods=['get', 'post'])
@login_required
@student_only # your security check
def create_review(lecturer_id):
    """
    handles the review creation page.
    """
    
    # get the lecturer (or 404) and make sure they are a lecturer
    lecturer = user.query.filter_by(id=lecturer_id, user_type='lecturer').first_or_404()
    
    # get all subjects to show in a dropdown
    all_subjects = subject.query.all()

    # --- post logic (when user submits the form) ---
    if request.method == 'post':
        try:
            # get all 5 ratings from your app.py model
            clarity = int(request.form.get('rating_clarity'))
            engagement = int(request.form.get('rating_engagement'))
            punctuality = int(request.form.get('rating_punctuality'))
            helpfulness = int(request.form.get('rating_helpfulness'))
            workload = int(request.form.get('rating_workload'))
            
            review_text = request.form.get('review_text').strip()
            subject_id = int(request.form.get('subject_id'))

            # validation
            ratings = [clarity, engagement, punctuality, helpfulness, workload]
            if not all(1 <= r <= 5 for r in ratings):
                flash('all ratings must be between 1 and 5.', 'error')
            elif len(review_text) < 20:
                flash('review must be at least 20 characters.', 'error')
            else:
                # all good, save to db
                new_review = review(
                    review_text=review_text,
                    rating_clarity=clarity,
                    rating_engagement=engagement,
                    rating_punctuality=punctuality,
                    rating_helpfulness=helpfulness,
                    rating_workload=workload,
                    user_id=current_user.id, # from mock user
                    lecturer_id=lecturer.id, # from url
                    subject_id=subject_id
                )
                
                db.session.add(new_review)
                db.session.commit()
                
                flash(f'review for {lecturer.email} submitted!', 'success')
                # todo: redirect to jimmy's lecturer profile page
                return redirect(url_for('main.lecturer_profile', lecturer_id=lecturer.id))

        except Exception as e:
            db.session.rollback()
            flash(f'an error occurred: {e}', 'error')

    # --- get logic (when user first visits the page) ---
    # pass lecturer and subjects to the html form
    return render_template('create_review.html', lecturer=lecturer, subjects=all_subjects)