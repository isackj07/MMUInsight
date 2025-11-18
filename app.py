import os
from flask import Flask, render_template
from extensions import db, bcrypt
from models import User  
from auth import auth_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "isac_is_a_monkey67"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "database", "mmuinsight.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_bp)

@app.route("/")
def index():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)

