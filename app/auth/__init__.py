"""
learn flask auth
"""
# pylint: disable=invalid-name, too-few-public-methods

from flask import Blueprint
auth = Blueprint('auth', __name__)
from . import views
