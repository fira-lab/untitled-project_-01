"""
`Storage` module
"""

from pymongo import MongoClient, collection
from bson import ObjectId
from typing import Dict, Any, List
import uuid
from os import environ

class Storage:
    """
    A class for storing and managing data.

    Attributes:
        dbClient (private class attribute): MongoDb client
    
    """

    def __init__(self):
        """
        Initialize `Storage` class
        """
        DB_HOST = environ.get('DB_HOST', 'localhost')
        DB_PORT = environ.get('DB_PORT', '27017')
        DB_DATABASE = environ.get('DB_DATABASE', 'HackFellow')
        client = MongoClient(f'mongodb://{DB_HOST}:{DB_PORT}')
        self.__dbClient = client[DB_DATABASE]
        self.__userCollection = self.__dbClient['user']
        self.__reviewCollection = self.__dbClient['review']

    def add_user(self, user_credentials: Dict[str, Any]) -> bool:
        """
        creates a new user in the database

        args:
            user_credentials (Dict): A dictionary with user credentialise
        
        return:
            (bool): True if successful or False if failed
        """
        if user_credentials is None or not isinstance(user_credentials, dict):
            return False
        user_id = uuid.uuid4()
        user_credentials['_id'] = str(user_id)
        try:
            result = self.__userCollection.insert_one(user_credentials)
            return result.acknowledged
        except Exception:
            return False

    def get_user(self, email=None, user_id=None) -> Dict[str, Any]:
        """
        return user matching email

        args:
            email (str): user email
        
        return:
            user (dict): user details
        """
        if email:
            if type(email) is not str:
                return
            user = self.__userCollection.find_one({ 'email': email })
        elif user_id:
            if type(user_id) is not str:
                return
            try:
                user = self.__userCollection.find_one({ '_id': user_id })
            except Exception:
                return
        else:
            return
        return user
    

    def delete_user(self, user_id: str) -> bool:
        """
        deletes a user

        args:
            user_id (str): user id
        
        return:
            (bool): return result of operation
        """
        if not user_id or type(user_id) is not str:
            return False
        result = self.__userCollection.delete_one({ '_id': user_id })
        return result.acknowledged
    
    def update_user(self, user_id: str, user_details: Dict[str, Any]) -> bool:
        """
        update user details

        Args:
            user_id (str): user id
            user_details (dict): user fields to update

        Return:
            (bool): result of the operation
        """
        if not user_id or type(user_id) is not str:
            return False
        if user_details is None or not isinstance(user_details, dict):
            return False
        result = self.__userCollection.update_one({'_id': user_id}, {'$set': user_details})
        return result.acknowledged

    def add_review(self, review: Dict[str, Any]) -> bool:
        result = self.__reviewCollection.insert_one(review)
        return result.acknowledged

    def get_all_reviews(self) -> List[Dict[str, Any]]:
    """
    return all reviews

    return:
        reviews (list): list of all reviews
    """
    try:
        reviews = list(self.__reviewCollection.find())
    except Exception:
        return
    return reviews
