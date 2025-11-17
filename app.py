<<<<<<< HEAD
<<<<<<< HEAD
from flask import Flask
import os

from extensions import db, bcrypt

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'database', 'mmuinsight.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # optional

db.init_app(app)
bcrypt.init_app(app)

# Ensure models are registered with SQLAlchemy
from models import User, Subject, Review  # noqa: F401

from register import register_bp
app.register_blueprint(register_bp)

# Optional: run once to create tables
# with app.app_context():
#     db.create_all()

@app.get("/")
def index():
    return "MMUInsight is running"

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # run once if tables are missing
    app.run(debug=True)
=======
import os
=======
>>>>>>> 71c8bfaaed558d42e4f80d40d1448d4d9d8cf668
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

<<<<<<< HEAD
>>>>>>> cb8e6cd12b251fb984ee3982a778d8c8a686d6e8
=======

>>>>>>> 71c8bfaaed558d42e4f80d40d1448d4d9d8cf668
