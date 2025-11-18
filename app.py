import os
from flask import Flask, render_template, flash, get_flashed_messages
from flask_login import LoginManager, current_user

from extensions import db, bcrypt
from models import User, Subject, Review
from auth import auth_bp
from reviews import reviews_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "isac_is_a_monkey67"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'database', 'mmuinsight.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(reviews_bp)

@app.get("/")
def index():
    messages_html = ""
    for category, message in get_flashed_messages(with_categories=True):
        messages_html += f'<div class="alert alert-{category}">{message}</div>'
    
    if current_user.is_authenticated:
        lecturers = User.query.filter_by(user_type='lecturer').all()
        links = ""
        if current_user.user_type == 'student':
            links = '<h2>Lecturers:</h2><ul>' + ''.join([f'<li><a href="/create_review/{l.id}">Write review for {l.email}</a></li>' for l in lecturers]) + '</ul>'
        
        return f"""
        <style>
            .alert {{ padding: 10px; margin: 10px 0; border-radius: 4px; }}
            .alert-error {{ background-color: #f8d7da; color: #721c24; }}
            .alert-success {{ background-color: #d4edda; color: #155724; }}
        </style>
        {messages_html}
        <h1>MMUInsight Running</h1>
        <p>Logged in as: {current_user.email} ({current_user.user_type})</p>
        {links}
        <a href="/logout">Logout</a>
        """
    return '<a href="/login">Login</a> | <a href="/register">Register</a>'

if __name__ == "__main__":
    app.run(debug=True)