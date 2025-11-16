from flask import Blueprint, request, jsonify
from app import db, User, Review

# Blueprint for review routes
reviews_bp = Blueprint('reviews', __name__)

