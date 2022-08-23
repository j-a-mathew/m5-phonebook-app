# create function to check tokens for rightful access to content
# API handles data/content that we want to see

from functools import wraps
import secrets
from flask import request, jsonify, json # JSON = JavaScript oriented -- content JS can parse easily
import decimal

from models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1] # take token number and check if valid in headers dictionary at "x-access-token" key
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401 # return JSON item to return back to user

        try:
            current_user_token = User.query.filter_by(token = token).first() # go to User class and search for User with token and look for first instance of it
            print(token)
            print(current_user_token)
        except:
            owner = User.query.filter_by(token = token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
        