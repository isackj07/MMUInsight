from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from . import register  # important: loads register.py so its routes decorate auth_bp

