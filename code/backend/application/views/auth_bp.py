# Online Support Ticket
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains Login/Logout/Register API.

# --------------------  Imports  --------------------

import os
from flask import Blueprint, request
from flask_restful import Api, Resource
import json
from ..logger import logger
from ..responses import *
from ..models import Auth
from ..globals import TOKEN_VALIDITY, BACKEND_ROOT_PATH, DISCOURSE_API_KEY
from ..database import db
import time
from .user_utils import UserUtils
from ..common_utils import (
    token_required,
    admin_required,
    convert_img_to_base64,
    is_img_path_valid,
    hash_password,
    verify_password
)

from ..tasks import create_user
from sqlalchemy import or_

# --------------------  Code  --------------------


class AuthUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def update_auth_table(self, details: dict):
        """
        Usage
        -----
        Update auth table while logging in and creating new account

        Parameters
        ----------
        details : dict with user details

        Returns
        -------
        updated user object

        """
        user = None
        if details["operation"] == "login":
            user = Auth.query.filter(or_(Auth.username == details["username"], Auth.email == details["email"])).first()
            user.web_token = details["web_token"]
            user.is_logged = True
            user.token_created_on = int(time.time())
            user.token_expiry_on = details["token_expiry_on"]
            db.session.commit()

        if details["operation"] == "register":
            user = Auth(
                user_id=details["user_id"],
                email=details["email"],
                password=details["password"],
                role=details["role"],
                name=details["name"],
                username=details["username"],
            )
            try:
                if details["is_verified"] or details["role"] == "admin":
                    user.is_verified = True
                else:
                    user.is_verified = False
               
            except Exception:
                
                user.is_verified = False
            db.session.add(user)
            db.session.commit()

        if details["operation"] == "verify_user":
            user = Auth.query.filter_by(user_id=details["user_id"]).first()
            user.is_verified = True
            db.session.commit()

        if details["operation"] == "delete_user":
            user = Auth.query.filter_by(user_id=details["user_id"]).first()
            db.session.delete(user)
            db.session.commit()

        return user


auth_bp = Blueprint("auth_bp", __name__)
auth_api = Api(auth_bp)
auth_utils = AuthUtils()


class Login(Resource):
    def post(self):
        """
        Usage
        -----
        For the user login page. It checks user data and raise appropriate error
        if required. Else it generates user token and returns it.

        Parameters
        ----------
        form data sent with request
        data format {'email':'', 'password':''}

        Returns
        -------
        User web token

        """
        form = {}

        # get form data
        try:
            form = request.get_json()
            email = form.get("email", "")
            username = form.get("username", "")
            password = form.get("password", "")
        except Exception as e:
            logger.error(f"Login->post : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            details = {"email": email, "username": username, "password": password, "operation": "login"}

            # verify form data
            is_email_valid = auth_utils.is_email_valid(email)
            is_username_valid = auth_utils.is_username_valid(username)
            if ((is_email_valid or is_username_valid) and auth_utils.is_password_valid(
                password
            )):
                # check if user exists
                user = None
                if(is_email_valid):
                    user = Auth.query.filter_by(email=email).first()
                else:
                    user = Auth.query.filter_by(username=username).first()
                if user:
                    # user exists
                    user_id = user.user_id

                    if verify_password(user.password, password):
                        # password is correct so log in user if user is verified
                        if user.is_verified or user.role == "admin":
                            #  generate token
                            token_expiry_on = int(int(time.time()) + TOKEN_VALIDITY)
                            # token_expiry_on = TOKEN_VALIDITY
                            web_token = auth_utils.generate_web_token(
                                email, token_expiry_on
                            )
                            details["web_token"] = web_token
                            details["token_expiry_on"] = token_expiry_on
                           
                            # update auth table
                            user = auth_utils.update_auth_table(details=details)

                            # get profile pic
                            profile_pic = user.profile_photo_loc
                            if profile_pic == "":
                                profile_pic = os.path.join(
                                    BACKEND_ROOT_PATH,
                                    "databases",
                                    "images",
                                    "profile_pics",
                                    "dummy_profile.png",
                                )
                            img_base64 = ""
                            if is_img_path_valid(profile_pic):
                                img_base64 = convert_img_to_base64(profile_pic)

                            logger.info("User logged in.")
                            return success_200_custom(
                                data={
                                    "user_id": user_id,
                                    "web_token": web_token,
                                    "token_expiry_on": token_expiry_on,
                                    "token_validity" : TOKEN_VALIDITY,
                                    "role": user.role,
                                    "name": user.name,
                                    "username": user.username,
                                    "email": user.email,
                                    "profile_photo_loc": img_base64,
                                }
                            )
                        else:
                            # user details are correct but user is not verified by admin
                            raise Unauthenticated(
                                status_msg="User is not verified by Admin."
                            )
                    else:
                        # password is wrong
                        raise Unauthenticated(status_msg="Password is incorrect")
                else:
                    # user does not exists
                    raise NotFoundError(status_msg="User does not exists")
            else:
                # email or password are not valid as per specification
                raise BadRequest(
                    status_msg="Email or Password are not valid as per specification"
                )


class Register(Resource):
    def post(self):
        """
        Usage
        -----
        For the user register page. It checks user data and raise appropriate error
        if required. Created user account and it generates user token and returns it. 

        Parameters
        ----------
        form data sent with request
        data format {'name':'', 'username':'', 'email':'',
                    'password':'', 'retype_password':'', 'role':''}
        'username' is optional

        Returns
        -------
        User web token

        """

        details = {
            "name": "",
            "username": "",
            "email": "",
            "password": "",
            "role": "",
            "is_verified": False
        }

        # get form data
        try:
            form = request.get_json()
        except Exception as e:
            logger.error(
                f"Register->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            for key in details:
                value = form.get(key, details[key])
                details[key] = value
                if auth_utils.is_blank(value):
                    raise BadRequest(status_msg=f"{key} is empty or invalid")
            details["operation"] = "register"

            # verify registration form data
            if auth_utils.verify_register_form(details):
                # check if user exists
                user = Auth.query.filter_by(email=details["email"]).first()
                username_exists = Auth.query.filter_by(username=details["username"]).first()
                if user:
                    # user exists means email is already in use
                    raise AlreadyExistError(status_msg="Email is already in use")
                elif username_exists:
                    # username is already in use
                    raise AlreadyExistError(status_msg="Username is already in taken")
                else:
                    # generate unique user_id
                    user_id = auth_utils.generate_user_id(email=details["email"])

                    # create new user in Auth table
                    details["user_id"] = user_id
                    temp = details["password"]
                    details["password"] = hash_password(temp)
                    details["unhashed_password"] = temp

                    user = auth_utils.update_auth_table(details=details)

                    ## Creates a discord user Asyncly
                    create_user.delay(details)

                    logger.info("New account created")
                    raise Success_200(
                        status_msg="Account created successfully. Now please login."
                    )

            else:
                # email or password are not valid as per specification
                raise BadRequest(
                    status_msg="Email or Password are not valid as per specification OR Password did not match."
                )


class NewUsers(Resource):
    # Admin access required
    # get user_id and token from headers
    # verify token and role of the user

    @token_required
    @admin_required
    def get(self):
        """
        Usage
        -----
        Get all new users which are not verified.
        Only admin can access this.

        Parameters
        ----------

        Returns
        -------
        New users dict

        """

        # get new users data from auth table
        try:
            all_users = (
                Auth.query.filter(Auth.role.in_(["student", "support"]))
                .filter_by(is_verified=False)
                .all()
            )
        except Exception as e:
            logger.error(f"NewUsers->get : Error occured while fetching db data : {e}")
            raise InternalServerError
        else:
            # convert to list of dict
            data = []
            for user in all_users:
                _d = {}
                _d["user_id"] = user.user_id
                _d["name"] = user.name
                _d["username"] = user.username
                _d["email"] = user.email
                _d["role"] = user.role
                data.append(_d)
            return success_200_custom(data=data)

    @token_required
    @admin_required
    def put(self, user_id):
        """
        Usage
        -----
        When admin verifies user, update user.is_verified to True in auth table

        Parameters
        ----------

        Returns
        -------

        """
        # get form data
        try:
            form = request.get_json()
            user_id = form.get("user_id", "")
        except Exception as e:
            logger.error(f"NewUsers->put : Error occured while getting form data : {e}")
            raise InternalServerError
        else:
            if auth_utils.is_blank(user_id):
                raise BadRequest(status_msg=f"User id is empty or invalid")

            details = {"user_id": user_id, "operation": "verify_user"}

            # check if user exists
            user = Auth.query.filter_by(user_id=user_id).first()
            if user:
                # user exists , proceed to update
                user = auth_utils.update_auth_table(details=details)
                raise Success_200(status_msg="User verified and updated in database.")
            else:
                raise NotFoundError(status_msg="User does not exists.")

    @token_required
    @admin_required
    def delete(self, user_id):
        """
        Usage
        -----
        When admin rejects user, update user.is_verified to False in auth table

        Parameters
        ----------

        Returns
        -------

        """
        # get form data
        try:
            form = request.get_json()
            user_id = form.get("user_id", "")
        except Exception as e:
            logger.error(
                f"NewUsers->delete : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            if auth_utils.is_blank(user_id):
                raise BadRequest(status_msg=f"User id is empty or invalid")
            details = {"user_id": user_id, "operation": "delete_user"}

            # check if user exists
            user = Auth.query.filter_by(user_id=user_id).first()
            if user:
                # user exists , proceed to update
                user = auth_utils.update_auth_table(details=details)
                raise Success_200(
                    status_msg="Verification failed so user deleted in database."
                )

                delete_user.delay(username=user.username)
            else:
                raise NotFoundError(status_msg="User does not exists.")


auth_api.add_resource(Login, "/login")  # path is /api/v1/auth
auth_api.add_resource(Register, "/register")
auth_api.add_resource(NewUsers, "/newUsers", "/newUsers/<string:user_id>")

# --------------------  END  --------------------
