from flask import Flask, jsonify

app = Flask(__name__)

# MOCK DATABASE
reviews_db = [
    {
        "id": 1, 
        "user_id": 1, 
        "lecturer_id": 101, 
        "subject_id": "CSP1123",
        "text": "GOATED class!",

        # RATING CATEGORIES
        "rating_clarity": 5,
        "rating_engagement": 5,
        "rating_punctuality": 4
    },
    {
        "id": 2, 
        "user_id": 2, 
        "lecturer_id": 102,
        "subject_id": "CMT1114",
        "text": "Informative lectures.",
        "rating_clarity": 3,
        "rating_engagement": 4,
        "rating_punctuality": 5
    }
]

# 3. MOCK USER TO TEST WITHOUT MING HAO
current_user = {"id": 1, "username": "Isac"}