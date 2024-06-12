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

from ..tasks import create_user, delete_user
from sqlalchemy import or_
from ..getters import get_user_id
class AllUtils(UserUtils):
    def update_user_profile_data(self, user_id, form):
        # check url data
        file_path = ""
        if self.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        details = {
            "name": "",
            "previous_password": "",
            "new_password": "",
            "profile_photo_loc": "",
        }
        # checks form data
        try:
            for key in details:
                value = form.get(key, "")
                if self.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(f"UserUtils : Error occured while getting form data : {e}")
            raise InternalServerError

        user = Auth.query.filter_by(user_id=user_id).first()
        if not user:
            raise NotFoundError(status_msg="User does not exists")
        role = user.role
        # checks if name is empty
            # check password
        
        if((details["new_password"] != "") and (details["previous_password"] != "")):
            # verify password
            print("here")
            if verify_password(user.password, details["previous_password"]):
                user.password = hash_password(details["new_password"])
            else:
                raise BadRequest(status_msg=f"Previous Password is invalid.")

            # update profile photo
        if details["profile_photo_loc"] != "":
            if details["profile_photo_loc"].startswith("data:image") and is_base64(
                details["profile_photo_loc"].split(",")[1]
            ):
                file_type, file_format, encoded_data = get_encoded_file_details(details["profile_photo_loc"])
                if (file_type == "image") and (file_format in ACCEPTED_IMAGE_EXTENSIONS):
                    file_name = f"{user_id}.{file_format}"
                    file_path = os.path.join(PROFILE_PIC_PATH, file_name)
                    print("here")
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
        logger.info("User details Updated successfully.")
        raise Success_200(status_msg="User details Updated successfully.")

all_utils = AllUtils()

user_bp = Blueprint("user_bp", __name__)

class UsersAPI(Resource):

    @user_bp.route('/all', methods=['GET'])
    @token_required
    @admin_required
    def get():
        try:
            all_users = (
                Auth.query.filter(Auth.role.in_(["student", "support"]))
                .filter_by(is_verified=True)
                .all()
            )
        except Exception as e:
            logger.error(f"Users->get : Error occured while fetching db data : {e}")
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
    
    @user_bp.route('/<string:user_id>', methods=['DELETE'])
    @token_required
    @admin_required
    def delete(user_id):
        try:
            user_id = user_id
        except Exception as e:
            logger.error(
                f"Users->delete : Error occured while getting data : {e}"
            )
            raise InternalServerError
        else:
            # check if user exists
            user = Auth.query.filter_by(user_id=user_id).first()
            if user:
                # user exists , proceed to delete
                db.session.delete(user)
                db.session.commit()
                delete_user.delay(username=user.username)
                raise Success_200(
                    status_msg="user deleted"
                )
            else:
                raise NotFoundError(status_msg="User does not exists.")

    @user_bp.route('/profile', methods=['PUT'])
    @token_required
    def put():
        try:
            form = request.get_json()
            user_id = get_user_id()
        except Exception as e:
            logger.error(f"UsersAPI->put : Error occured while getting form data : {e}")
            raise InternalServerError

        all_utils.update_user_profile_data(user_id, form)
