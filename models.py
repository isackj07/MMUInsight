from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
<<<<<<< HEAD
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(10), nullable=False, default='student') # 'student' or 'lecturer'
=======
    password_hash = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(10), nullable=False, default='student') 
>>>>>>> b45f8209d4b7392c662abcedc5fd44dc57afe4ee
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    verification_token = db.Column(db.String(100), nullable=True)
<<<<<<< HEAD

    reviews_written = db.relationship('Review', foreign_keys='Review.user_id', backref='author', lazy=True)
    reviews_received = db.relationship('Review', foreign_keys='Review.lecturer_id', backref='lecturer', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(20), unique=True, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)

    reviews = db.relationship('Review', backref='subject', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.Text, nullable=False)
    rating_clarity = db.Column(db.Integer, nullable=False)
    rating_engagement = db.Column(db.Integer, nullable=False)
    rating_punctuality = db.Column(db.Integer, nullable=False)
    rating_helpfulness = db.Column(db.Integer, nullable=False)
    rating_workload = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

=======
    reset_token = db.Column(db.String(100), nullable=True)
>>>>>>> b45f8209d4b7392c662abcedc5fd44dc57afe4ee
