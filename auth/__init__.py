from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from . import register, login, logout, verify, reset_password, routes
