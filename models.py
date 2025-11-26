from flask_login import UserMixin
from extensions import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(10), nullable=False, default='student')
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    verification_token = db.Column(db.String(100), nullable=True)
    reset_token = db.Column(db.String(100), nullable=True)

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
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)
