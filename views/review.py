from flask import Flask, request, jsonify, session, redirect, url_for, make_response
from views import review_views
from models.db import Storage
from models.sentiment_analysis import SentimentAnalysis

storage = Storage()
sentimentAnalysis = SentimentAnalysis()

@review_views.route('/add', methods = ['POST'], strict_slashes=False)
def add_review():
    """
    add review to database

    args:
        review (dict): review details
    """
    review = request.get_json()
    if not review:
        return make_response(jsonify({ 'error': 'invalid request' }), 400)
    if 'feedback' not in review:
        return make_response(jsonify({ 'error': 'invalid request' }), 400)
    review['sentiment'] = sentimentAnalysis.analyse(review['feedback'])[0]['label']
    result = storage.add_review(review)
    if result:
        return make_response(jsonify({ 'message': 'review added' }), 201)
    return make_response(jsonify({ 'error': 'could not add review' }), 500) 