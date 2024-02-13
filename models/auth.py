from models.db import Storage
from flask import request, session
from functools import wraps
import bcrypt

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if session_id not in session:
            return redirect(url_for('root'))
        return func(*args, **kwargs)
    return wrapper


class AuthManager:
    def __init__(self):
        self.storage = Storage()

    def create_user(self, email, password, **kwargs):
        # Check if the email already exists
        existing_user = self.storage.get_user(email)
        if existing_user:
            return False  # Username already exists

        # Hash the password
        hashed_password = self._hash_password(password)

        # Add the user to the storage
        user_credentials = {'email': email, 'password': hashed_password, **kwargs}
        return self.storage.add_user(user_credentials)

    def check_password(self, email, password):
        # Retrieve the user from the storage
        user = self.storage.get_user(email)
        if not user:
            return False  # User not found

        # Verify the password
        hashed_password = user.get('password', '')
        return self._verify_password(password, hashed_password)

    def get_user(self, email):
        return self.storage.get_user(email)

    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def _verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


