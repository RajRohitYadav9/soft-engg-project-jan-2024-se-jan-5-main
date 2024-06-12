# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is common utils file. All common and
# independent functions will be here.
import hashlib
# --------------------  Imports  --------------------
from flask import current_app as app
from functools import wraps

import jwt
from flask import request
from .getters import get_user_id, get_web_token
from .responses import *
from .logger import logger
from .models import Auth
from .globals import *
import base64
from .database import db
import time
import bcrypt
# --------------------  Code  --------------------


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            frontend_token = get_web_token()
            user_id_rec = get_user_id()  # user_id sent by frontend
        except Exception as e:
            logger.error(f"Error occured while checking request token : {e}")
            raise InternalServerError
        else:
            user = Auth.query.filter_by(user_id=user_id_rec).first()
            if user:
                if user.is_logged:
                    # if token is expired then update auth table and ask user to login again
                    if int(time.time()) > user.token_expiry_on:
                        user.is_logged = False
                        user.web_token = ""
                        user.token_created_on = 0
                        user.token_expiry_on = 0
                        db.session.add(user)
                        db.session.commit()
                        raise Unauthenticated(
                            status_msg="Token is expired. Please login again."
                        )

                    if frontend_token:
                        # check token
                        backend_token = user.web_token
                        if frontend_token == backend_token:
                            # token is correct
                            logger.info(
                                f"Token is verified for the user: {user_id_rec}"
                            )
                            return f(*args, **kwargs)
                        else:
                            raise Unauthenticated(status_msg="Token is incorrect")
                    else:
                        # token is empty
                        raise Unauthenticated(status_msg="Token is empty or missing")
                else:
                    raise Unauthenticated(
                        status_msg="Access denied. User is not logged in."
                    )
            else:
                raise NotFoundError(
                    status_msg="Provided used id does not exists. Please create account."
                )

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            user_id_rec = get_user_id()  # user_id sent by frontend
        except Exception as e:
            logger.error(f"Error occured while checking user id : {e}")
            raise InternalServerError
        else:
            role = Auth.query.filter_by(user_id=user_id_rec).first().role
            if role == "admin":
                # role verified
                logger.info(f"Admin role is verified for the user: {user_id_rec}")
                return f(*args, **kwargs)
            else:
                raise Unauthenticated(
                    status_msg="Access denied. Only admin can access this endpoint."
                )

    return decorated


def users_required(users:list):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                user_id_rec = get_user_id() # user_id sent by frontend
            except Exception as e:
                logger.error(f"Error occured while checking user id : {e}")
                raise InternalServerError
            else:
                user = Auth.query.filter_by(user_id=user_id_rec).first()
                if user:
                    role = user.role
                    if role in users:
                        # role verified
                        if user.is_verified or role == "admin":
                            logger.info(
                                f"User role : {role} : is verified for the user: {user_id_rec}"
                            )
                            return f(*args, **kwargs)
                        else:
                            raise Unauthenticated(status_msg="User is not verified.")
                    else:
                        raise Unauthenticated(status_msg="Access denied.")
                else:
                    raise NotFoundError(status_msg="User does not exists")

        return decorated

    return decorator


def is_img_path_valid(img_path: str) -> bool:
    if os.path.isfile(img_path):
        if img_path.endswith(tuple(ACCEPTED_IMAGE_EXTENSIONS)):
            return True
        else:
            logger.info(f"File extension is not valid : {img_path}")
    else:
        logger.info(f"File path is not valid: {img_path}")
    return False


def convert_img_to_base64(img_path: str) -> str:
    try:
        with open(img_path, "rb") as img:
            img_base64 = base64.b64encode(img.read())
        img_base64 = str(img_base64, "UTF-8")
        extension = img_path.split(".")[-1]
        img_base64 = f"data:image/{extension};base64," + img_base64
        return img_base64
    except Exception as e:
        resp = f"Unknown error occured while converting image to base64: {e}"
        logger.error(resp)
        return ""


def convert_base64_to_img(img_path: str, img_base64: str) -> bool:
    try:
        with open(img_path, "wb") as img:
            img.write(base64.b64decode(img_base64))
        return True
    except Exception as e:
        resp = f"Unknown error occured while converting base64 to image: {e}"
        logger.error(resp)
        return False


def is_base64(string: str) -> bool:
    # check if string is base 64 encoded
    try:
        decoded_string = base64.b64decode(string)
        encoded_string = base64.b64encode(decoded_string)
        # encoded_string is in bytes format
        encoded_string = str(encoded_string, "UTF-8")
        if encoded_string == string:
            return True
        else:
            return False
    except Exception as e:
        logger.error("Error occured while checking string encode format: {e}")
        return False


def get_encoded_file_details(file_base64: str):
    # file type is whether its image or else
    # file format is like jpeg, jpg, png
    # encoded data is file encoding in base64
    # sample: "data:image/jpeg;base64,/9....."

    encoding_metadata, encoded_data = file_base64.split(",")[0:2]
    encoding_metadata = encoding_metadata.split(";")[0].split(":")[1]
    file_type, file_format = encoding_metadata.split("/")[:2]
    return file_type, file_format, encoded_data

def generate_user_id(email: str) -> str:
        """
        Usage
        -----
        Generate user id from email and hashing with md5

        Parameters
        ----------
        email : email id of user

        Returns
        -------
        user_id

        """
        # use email to generate unique id
        user_id = hashlib.md5(email.encode()).hexdigest()
        return user_id
def generate_web_token(email: str, token_expiry_on: int) -> str:
        """
        Usage
        -----
        Generate jwt token from email id

        Parameters
        ----------
        email : email id of user
        token_expiry_on : expiry timestamp

        Returns
        -------
        web_token

        """
        # use current time stamp and email to generate unique token
        web_token = jwt.encode(
            {
                "email": email,
                "expiry": token_expiry_on,
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return web_token



def hash_password(password):
    # Hash a password for the first time
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')  # Return the hashed password as a string

def verify_password(hashed_password, input_password):
    # Check a hashed password against an input password
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))
# --------------------  END  --------------------
