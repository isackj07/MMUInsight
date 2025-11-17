from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy #translator between python and db
from flask_bcrypt import Bcrypt 
import os 

# Initialize app and extensions
app = Flask(__name__)

# dev secret key – lowkey fucking ghetto method
app.config['SECRET_KEY'] = 'mmuinsight-dev-secret'
# (or: app.secret_key = 'mmuinsight-dev-secret')

# Configure the database (a local file) (i fixed this shit)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'database', 'mmuinsight.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

# Initialize the database manager (ORM)
db = SQLAlchemy(app)

# Initialize the password hasher
bcrypt = Bcrypt(app)


# This is the "blueprint" for our shared tables

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(10), nullable=False, default='student') # 'student' or 'lecturer'
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    verification_token = db.Column(db.String(100), nullable=True)
    
    # Relationship: Connects User to the reviews they have written
    reviews_written = db.relationship('Review', foreign_keys='Review.user_id', backref='author', lazy=True)
    # Relationship: Connects Lecturer to the reviews they have received
    reviews_received = db.relationship('Review', foreign_keys='Review.lecturer_id', backref='lecturer', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(20), unique=True, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    
    # Relationship: Connects a Subject to its reviews
    reviews = db.relationship('Review', backref='subject', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.Text, nullable=False)
    
    # --- These are your "Rating Categories" ---
    rating_clarity = db.Column(db.Integer, nullable=False)
    rating_engagement = db.Column(db.Integer, nullable=False)
    rating_punctuality = db.Column(db.Integer, nullable=False)
    rating_helpfulness = db.Column(db.Integer, nullable=False)
    rating_workload = db.Column(db.Integer, nullable=False)
    
    # These are the "links" (Foreign Keys) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # The student who wrote it
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # The lecturer being reviewed
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False) # The subject it's for

from register import register_bp
from verify import verify_bp

app.register_blueprint(register_bp)
app.register_blueprint(verify_bp)