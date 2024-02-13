from flask import Blueprint

auth_views = Blueprint("auth_views", __name__)
review_views = Blueprint("review_views", __name__)

from views.auth import *
from views.review import *