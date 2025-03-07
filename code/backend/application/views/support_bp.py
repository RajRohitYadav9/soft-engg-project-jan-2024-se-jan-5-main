# Online Support Ticket .
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Support Staff Blueprint file.

# --------------------  Imports  --------------------

from flask import Blueprint, request
from flask_restful import Api, Resource
from ..getters import get_user_id
from ..logger import logger
from ..common_utils import (
    token_required,
    users_required,
)
from .user_utils import UserUtils
from ..responses import *
from ..models import Auth, Ticket, Solution
from ..globals import *
from ..getters import get_username

# --------------------  Code  --------------------


class SupportUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id


support_bp = Blueprint("support_bp", __name__)
support_api = Api(support_bp)
support_util = SupportUtils()


class SupportAPI(Resource):
    @token_required
    @users_required(users=["support"])
    def get(self):
        """
        Usage
        -----
        Get a details of support team member from user_id

        Parameters
        ----------
        user id

        Returns
        -------
        details

        """
        user_id = get_user_id()
        if support_util.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # check if user exists
        try:
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"SupportAPI->get : Error occured while fetching support data : {e}"
            )
            raise InternalServerError
        else:
            if user:
                username = get_username(Auth,user_id)
                if user.role == "support":
                    n_tickets_resolved = Solution.query.filter_by(
                        resolved_by=username
                    ).count()
                    n_total_unresolved_tickets = Ticket.query.filter_by(
                        status="pending"
                    ).count()
                    support_dict = support_util.convert_user_data_to_dict(user)
                    support_dict["n_tickets_resolved"] = n_tickets_resolved
                    support_dict[
                        "n_total_unresolved_tickets"
                    ] = n_total_unresolved_tickets

                    return success_200_custom(data=support_dict)
                else:
                    raise BadRequest(status_msg="User must be a support staff.")
            else:
                raise NotFoundError(status_msg="Support staff does not exists")

    @token_required
    @users_required(users=["support"])
    def put(self):
        """
        Usage
        ------
        Update support profile,
        #support can update first name, last name, email, password, profile picture location
        ------
        Args:
            user_id (integer): id of user
        ------
        Parameters
        ------
        Form data send with request

        Returns
        ------
        """
        user_id = get_user_id()
        try:
            form = request.get_json()
        except Exception as e:
            logger.error(
                f"SupportAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            support_util.update_user_profile_data(user_id, form)


support_api.add_resource(SupportAPI,"")  # path is /api/v1/support

# support_api.add_resource(SupportAPI, "/<string:user_id>")  # path is /api/v1/support

# --------------------  END  --------------------
