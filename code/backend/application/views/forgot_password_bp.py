from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import url_for

import os
from flask import Blueprint, request
from flask_restful import Api, Resource
import json
from ..logger import logger
from ..responses import *
from ..models import Auth
from ..globals import *
from ..database import db
import time
from .user_utils import UserUtils
from ..common_utils import (
    token_required,
    admin_required,
    convert_img_to_base64,
    is_img_path_valid,
    hash_password,
    verify_password,
    convert_base64_to_img,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from ..tasks import async_send_forgot_password_email
from sqlalchemy import or_
from ..getters import get_user_id
from application import cache

forgot_password_bp = Blueprint("forgot_password_bp", __name__)

import random
import string

def generate_password(min_length=8, max_length=20):
  """Generates a random password with a minimum and maximum length.

  Args:
      min_length: The minimum length of the password (default: 8).
      max_length: The maximum length of the password (default: 20).

  Returns:
      A randomly generated password string.
  """
  lowercase_letters = string.ascii_lowercase
  uppercase_letters = string.ascii_uppercase
  digits = string.digits
  punctuation = string.punctuation

  character_pool = lowercase_letters + uppercase_letters + digits + punctuation

  password = [random.choice(lowercase_letters)]
  password.append(random.choice(uppercase_letters))
  password.append(random.choice(digits))
  password.append(random.choice(punctuation))

  password.extend(random.choices(character_pool, k=random.randint(min_length - 4, max_length - 4)))

  random.shuffle(password)

  return ''.join(password)



class VerifyEmailAPI(Resource):
    @forgot_password_bp.route("/forgot/<string:username>", methods=["POST"])
    @cache.cached(timeout=50)
    def post(username=""):
        user = Auth.query.filter_by(username = username).first()
        if user:
            password = generate_password()
            user.password = hash_password(password)
            db.session.add(user)
            db.session.commit()
            async_send_forgot_password_email.delay(user.email,password)
            return success_200_custom(data="check your email")
        raise BadRequest(status_msg="no user with this username")

