from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
<<<<<<< HEAD

from . import register  # important: loads register.py so its routes decorate auth_bp
=======
>>>>>>> b45f8209d4b7392c662abcedc5fd44dc57afe4ee

from . import register, login, logout, verify, reset_password, routes
