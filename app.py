from flask import Flask
import os

from extensions import db, bcrypt
from models import User, Subject, Review
from auth import auth_bp  # FIX

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'database', 'mmuinsight.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_bp)

@app.get("/")
def index():
    return "MMUInsight running"

if __name__ == "__main__":
    app.run(debug=True)


