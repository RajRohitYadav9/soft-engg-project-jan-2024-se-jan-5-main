# Online Support Ticket .
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains user class (common).

# --------------------  Imports  --------------------

import os
from flask import current_app as app
import jwt
import hashlib
from ..common_utils import (
    convert_base64_to_img,
    convert_img_to_base64,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from ..responses import *
from ..logger import logger
from ..models import *
from ..globals import *


# --------------------  Code  --------------------


class UserUtils:
    # def is_blank(self, string):
    #     # for "", "  ", None : True else False
    #     if string == "undefined":
    #         return True
    #     return not (bool(string and not string.isspace()))

    def is_blank(self, string_value):
        """
        Checks if the given value is considered "blank".

        Args:
            string_value (str or None): The value to be checked.

        Returns:
            bool: True if the value is considered blank, False otherwise.
        """

        # # Handle missing values first
        # # if string_value is None or len(string_value) == 0:
        # if string_value is None:
        #     return True

        # # Convert to string if necessary
        # try:
        #     string_value = str(string_value)
        # except (ValueError, TypeError):
        #     return True

        # # Check for emptiness or "undefined" case
        # return not any((string_value, isinstance(string_value, str) and not string_value.isspace(), string_value == "undefined"))

        return string_value is None or (isinstance(string_value, str) and not string_value.strip())


    def is_email_valid(self, email):
        is_valid = False
        # import re
        # regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        # is_valid = re.search(regex, email)
        # But to keep it simple for now
        if "@" in email:
            is_valid = True
        return is_valid

    def is_username_valid(self, username):
        is_valid = False
        # import re
        # regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        # is_valid = re.search(regex, email)
        # But to keep it simple for now
        return username != ""

    def is_password_valid(self, password):

        return True

    def verify_register_form(self, details: dict):
        """
        Usage
        -----
        verify user email, password while creating new account

        Parameters
        ----------
        details: dict

        Returns
        -------
        return boolean status

        """
        # verify email
        if not self.is_email_valid(details["email"]):
            return False

        # verify password
        if not self.is_password_valid(details["password"]):
            return False

        return True

    def generate_web_token(self, email: str, token_expiry_on: int) -> str:
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

    def generate_user_id(self, email: str) -> str:
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

    def convert_user_data_to_dict(self, user) -> dict:
        user_dict = dict(vars(user))
        if "_sa_instance_state" in user_dict:
            del user_dict["_sa_instance_state"]
        if "password" in user_dict:
            del user_dict["password"]
        profile_pic = user_dict["profile_photo_loc"]
        if is_img_path_valid(profile_pic):
            img_base64 = convert_img_to_base64(profile_pic)
            if img_base64 != "":
                user_dict["profile_photo_loc"] = img_base64
            else:
                user_dict["profile_photo_loc"] = ""
        else:
            user_dict["profile_photo_loc"] = ""
        return user_dict

    def update_user_profile_data(self, user_id, form):
        # check url data
        file_path = ""
        if self.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        details = {
            "name": "",
            "email": "",
            "password": "",
            "profile_photo_loc": "",
        }

        # checks form data
        try:
            for key in details:
                value = form.get(key, "")
                if self.is_blank(value):
                    value = ""
                details[key] = value
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(f"UserUtils : Error occured while getting form data : {e}")
            raise InternalServerError

        else:
            # User doesn't exist
            if not user:
                raise NotFoundError(status_msg="User does not exists")

            role = user.role

            # checks if first name is empty
            if self.is_blank(details["name"]):
                raise BadRequest(status_msg=f"Name is required")
            else:
                user.name = details["name"]

            # checks if email is valid
            if not (self.is_email_valid(details["email"])):
                raise BadRequest(status_msg=f"Email is required annd should be valid.")
            else:
                user_ = Auth.query.filter_by(email=details["email"]).first()
                if user_:
                    # if user id dont match means email already in use
                    if user_.user_id != user.user_id:
                        raise AlreadyExistError(status_msg="Email is already in use")
                else:
                    user.email = details["email"]

            # check password
            if not self.is_blank(details["password"]):
                # verify password
                if self.is_password_valid(details["password"]) and (
                    details["password"] == details["retype_password"]
                ):
                    user.password = details["password"]
                else:
                    raise BadRequest(status_msg=f"Password is invalid.")

            # update profile photo
            if details["profile_photo_loc"] != "":
                if details["profile_photo_loc"].startswith("data:image") and is_base64(
                    details["profile_photo_loc"].split(",")[1]
                ):
                    file_type, file_format, encoded_data = get_encoded_file_details(
                        details["profile_photo_loc"]
                    )
                    if (file_type == "image") and (
                        file_format in ACCEPTED_IMAGE_EXTENSIONS
                    ):
                        file_name = f"{user_id}.{file_format}"
                        file_path = os.path.join(PROFILE_PIC_PATH, file_name)
                    if convert_base64_to_img(file_path, encoded_data):
                        # successfully image saved and now add entry to database
                        user.profile_photo_loc = file_path

            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                logger.error(
                    f"UserUtils->put : Error occured while updating user details : {e}"
                )
                raise InternalServerError(
                    status_msg="Error occured while updating user details"
                )
            else:
                logger.info("User details Updated successfully.")
                raise Success_200(status_msg="User details Updated successfully.")


# --------------------  END  --------------------
