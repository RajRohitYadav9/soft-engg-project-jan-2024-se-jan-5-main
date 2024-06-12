# Online Support Ticket .
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Ticket Blueprint file.

# --------------------  Imports  --------------------

import hashlib
import time
from flask import Blueprint, request
from flask_restful import Api, Resource
from ..logger import logger
from ..common_utils import (
    token_required,
    users_required,
    admin_required,
    convert_base64_to_img,
    convert_img_to_base64,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from ..getters import get_user_id
from .user_utils import UserUtils
from ..responses import *
from ..models import *
from copy import deepcopy
from ..globals import *
from ..getters import get_username
from ..notifications import send_email
from ..tasks import create_user, create_ticket, create_reply, async_send_email, request_discourse_accept, request_discourse_unaccept, delete_ticket, send_gchat_notification

# from celery import shared_task
# --------------------  Code  --------------------


class TicketUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def convert_ticket_to_dict(self, ticket):
        ticket_dict = dict(vars(ticket))  # verify if this properly converts obj to dict
        ticket_dict["tags"] = ticket.tags.split(",")
        if(ticket.solution_id != -1):
            solution = ticket.solution
            ticket_dict["solution"] = solution.description
            ticket_dict["resolved_by"] = solution.resolved_by
            ticket_dict["resolved_on"] = solution.resolved_on
        print("Extra Printing Here", ticket_dict)
        if "_sa_instance_state" in ticket_dict:
            del ticket_dict["_sa_instance_state"]
        ticket_attachments = self.get_ticket_attachments(ticket_id=ticket.ticket_id)
        ticket_dict["ticket_attachments"] = ticket_attachments
        reply_attachments = self.get_solution_attachments(solution_id=ticket.solution_id)
        ticket_dict["reply_attachments"] = reply_attachments
        return ticket_dict

    def get_attachments(self,attachment_list : list) -> list:
        attachments = []
        for att in attachment_list:
            file_path = att.attachment_loc
            img_base64 = ""
            if is_img_path_valid(file_path):
                img_base64 = convert_img_to_base64(file_path)
            d_ = {"user_id": att.user_id, "attachment_loc": img_base64}
            attachments.append(d_)
        return attachments

    def get_ticket_attachments(self, ticket_id):
        ticket_attach = TicketAttachment.query.filter_by(ticket_id=ticket_id).all()
        attachments = self.get_attachments(ticket_attach)
        return attachments

    def get_solution_attachments(self, solution_id):
        sol_attach = SolutionAttachment.query.filter_by(solution_id=solution_id).all()
        attachments = self.get_attachments(sol_attach)
        return attachments

    def generate_ticket_id(self, title: str, user_id: str) -> str:
        """
        Ticket id is generated from ticket title and user id and timestamp
        """
        # generate unique id
        ts = str(int(time.time_ns()))
        string = f"{user_id}_{title}_{ts}"
        ticket_id = hashlib.md5(string.encode()).hexdigest()
        return ticket_id

    
    def save_attachments(
        self, attachments: list, attachment_id: str, user_id: str, attachment_type: str
    ):

        # get list of files from db for the ticket and user
        # if file already exists then add number extension
        # file name is not saved , only number extension required
        # currently there is no option to delete attachment
        # file name: {ticket_id}_{user_id}_{number-extension-if-needed}_.{file_format}
        # operation : create_ticket , update_ticket only student can do | resolve_ticket only support can do.

        total_attachments = len(attachments)
        num_successful_attachments = 0

        if total_attachments == 0:
            return False, "Attachments are empty."

        files = [
            file
            for file in os.listdir(TICKET_ATTACHMENTS_PATH)
            if file.startswith(f"{attachment_id}_{user_id}")
        ]
        number_extension = len(files)  # starting point

        for attach in attachments:
            # attach will be of format {attachment_loc:'', user_id:''}
            # attachment_loc will contain base64 version of image while data transfer is occuring
            # between backend and frontend
            # attachment_loc will contain image path when data is retried from db by backend
            # attachment_loc will contain base64 image when creating new attachment

            if attach["attachment_loc"]:
                if is_base64(attach["attachment_loc"].split(",")[1]):
                    file_type, file_format, encoded_data = get_encoded_file_details(
                        attach["attachment_loc"]
                    )
                    if (file_type == "image") and (
                        file_format in ACCEPTED_IMAGE_EXTENSIONS
                    ):
                        file_name = (
                            f"{attachment_id}_{user_id}_{number_extension}.{file_format}"
                        )
                        file_path = os.path.join(TICKET_ATTACHMENTS_PATH, file_name)
                        if convert_base64_to_img(file_path, encoded_data):
                            # successfully image saved and now add entry to database
                            try:
                                # while creating a ticket a student can upload multiple attachments
                                # verify whether each attachment is unique
                                attach["attachment_loc"] = file_path
                                if (attachment_type=="ticket"):
                                    attach["ticket_id"] = attachment_id
                                    ticket_attach = TicketAttachment(**attach)
                                    db.session.add(ticket_attach)
                                else:
                                    attach["solution_id"] = attachment_id
                                    solution_attach = SolutionAttachment(**attach)
                                    db.session.add(solution_attach)
                                db.session.commit()
                                num_successful_attachments += 1
                                number_extension += 1
                            except Exception as e:
                                logger.error(
                                    f"TicketAPI->post : Error occured while creating a Ticket Attachment : {e}"
                                )
        return (
            True,
            f"Total {num_successful_attachments} / {total_attachments} attchements are valid and added successfully.",
        )

    def save_ticket_attachments(
        self, attachments: list, ticket_id: str, user_id: str, operation: str
    ):
        # get list of files from db for the ticket and user
        # if file already exists then add number extension
        # file name is not saved , only number extension required
        # currently there is no option to delete attachment
        # file name: {ticket_id}_{user_id}_{number-extension-if-needed}_.{file_format}
        # operation : create_ticket , update_ticket only student can do | resolve_ticket only support can do.

        return self.save_attachments(attachments,ticket_id,user_id,attachment_type="ticket")
    def save_solution_attachments(
        self, attachments: list, solution_id: str, user_id: str, operation: str
    ):
        # get list of files from db for the ticket and user
        # if file already exists then add number extension
        # file name is not saved , only number extension required
        # currently there is no option to delete attachment
        # file name: {ticket_id}_{user_id}_{number-extension-if-needed}_.{file_format}
        # operation : create_ticket , update_ticket only student can do | resolve_ticket only support can do.

        return self.save_attachments(attachments,solution_id,user_id,attachment_type="solution")

    def tickets_filter_by_query(self, all_tickets, query=""):
        # match tickets with query
        filtered_tickets = []
    
        if query != "":
            for ticket in all_tickets:
                search_in = ("")
                try:
                    search_in = (
                        f"{ticket['title']} {ticket['description']} {ticket['solution']}"
                    )
                except:
                    search_in = (
                        f"{ticket['title']} {ticket['description']}"
                    )
                for q in query.split(" "):
                    if q.lower() in search_in.lower():
                        filtered_tickets.append(ticket)
                        break

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_tags(self, all_tickets, tags=[]):
        # filter by tags (if present)
        filtered_tickets = []
        if tags:
            for ticket in all_tickets:
                print(set(ticket["tags"]),set(tags))
                if set(ticket["tags"]).intersection(set(tags)):
                    filtered_tickets.append(ticket)
            print(filtered_tickets)
            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_status(self, all_tickets, status=[]):
        # filter by status (if present)
        filtered_tickets = []
        if status:
            for ticket in all_tickets:
                if ticket["status"] in status:
                    filtered_tickets.append(ticket)

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_priority(self, all_tickets, priority=[]):
        # filter by priority (if present)
        filtered_tickets = []
        if priority:
            for ticket in all_tickets:
                if ticket["priority"] in priority:
                    filtered_tickets.append(ticket)

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_sort(self, all_tickets, sortby="", sortdir=""):
        # sort (if present)
        if sortby:
            # sortby should be 'created_on', 'resolved_on', 'votes'
            if sortby not in ["created_on", "resolved_on", "votes"]:
                sortby = "created_on"
        else:
            sortby = "created_on"
        if sortdir:
            # sortdir should be 'asc' or 'desc'
            sortdir = True if sortdir == "desc" else False
        else:
            sortdir = True
        all_tickets = sorted(all_tickets, key=lambda d: d[sortby], reverse=sortdir)
        return all_tickets

    def tickets_filter_sort(self, all_tickets, args):
        # match tickets with query
        all_tickets = self.tickets_filter_by_query(all_tickets, args["query"])

        # filter by tags (if present)
        all_tickets = self.tickets_filter_by_tags(all_tickets, args["tags"])

        # filter by status (if present)
        all_tickets = self.tickets_filter_by_status(all_tickets, args["status"])

        # filter by priority (if present)
        all_tickets = self.tickets_filter_by_priority(all_tickets, args["priority"])

        # sort (if present)
        all_tickets = self.tickets_sort(all_tickets, args["sortby"], args["sortdir"])

        return all_tickets

    def get_args_from_query(self, args):
        def convert_arg_to_list(arg: str):
            # for internal use only
            arg = args.get(arg, "")
            if arg == "":
                return []
            else:
                return arg.split(",")

        _args = {"query": args.get("query", ""), "sortby": args.get("sortby", ""), "sortdir": args.get("sortdir", ""),
                 "status": convert_arg_to_list("filter_status"), "priority": convert_arg_to_list("filter_priority"),
                 "tags": convert_arg_to_list("filter_tags")}

        return _args


ticket_bp = Blueprint("ticket_bp", __name__)
ticket_api = Api(ticket_bp)
ticket_utils = TicketUtils()


class TicketAPI(Resource):
    @token_required
    @users_required(users=["student", "support", "admin"])
    def get(self, ticket_id=""):
        """
        Usage
        -----
        Get a single ticket for the user and return

        Parameters
        ----------
        ticket is

        Returns
        -------
        Ticket

        """
        user_id = request.headers.get('User-Id',"")
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                user = Auth.query.filter_by(user_id=user_id).first()
                # if user_id == ticket.owner_id or user.role == "support":
                    # the ticket and its user are matched or its a support staff
                    # convert to list of dict
                ticket_dict = ticket_utils.convert_ticket_to_dict(ticket)
                return success_200_custom(data=ticket_dict)
            else:
                raise NotFoundError(status_msg="Ticket does not exists")

    @token_required
    @users_required(users=["student"])
    def post(self):
        """
        Usage
        -----
        Create a new ticket. Only a student can create.

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """
        details = {
            "title": "",
            "description": "",
            "tags": "",
            "privacy": "",
        }
        user_id = request.headers.get('User-Id',"")
        username = ""
        # check user_id
        if ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id is empty/missing in url")

        try:
            user = Auth.query.filter_by(user_id=user_id).first()
            username = user.username
            if not user:
                # user id does not exists
                raise NotFoundError(status_msg="User id does not exists.")
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # get form data
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
            for key in details:
                value = form.get(key, "")
                if ticket_utils.is_blank(value):
                    value = ""
                details[key] = value
            details["tags"] = ",".join(details["tags"])
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            if details["title"] == "" or details["tags"] == "":
                raise BadRequest(
                    status_msg=f"Ticket title and at least one tag is required"
                )

            ticket_id = ticket_utils.generate_ticket_id(details["title"], user_id)
            details["ticket_id"] = ticket_id
            details["owner_id"] = user_id
            details["created_by"] = username
            details["created_on"] = int(time.time())
            ticket = Ticket(**details)

            if details["privacy"] == "public":
                create_ticket.delay(api_username=username,ticket_obj = details)
            try:
                db.session.add(ticket)
                db.session.commit()
            except Exception as e:
                logger.error(
                    f"TicketAPI->post : Error occured while creating a new ticket : {e}"
                )
                raise InternalServerError(
                    status_msg="Error occured while creating a new ticket"
                )
            else:
                logger.info("Ticket created successfully.")

                # add attachments now
                status, message = ticket_utils.save_ticket_attachments(
                    attachments, ticket_id, user_id, operation="create_ticket"
                )
                raise Success_200(status_msg=f"Ticket created successfully. {message}")

    @token_required
    @users_required(users=["student", "support"])
    def put(self, ticket_id=""):
        """
        Usage
        -----
        Update a ticket.
        only student and support has access, role is checked later in code.
        Student who created a ticket can update : title, description, attachments, tags, priority
        Student who did not create : can vote a ticket
        Support can update : solution and attachment, status

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """
        details = {
            "title": "",
            "description": "",
            "tags": "",
            "privacy": ""
        }
        user_id = request.headers.get('User-Id',"")
        # check url data
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check form data
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
            for key in details:
                value = form.get(key, "")
                if ticket_utils.is_blank(value):
                    value = ""
                details[key] = value
            details["tags"] = ",".join(details["tags"])
        except Exception as e:
            logger.error(
                f"TicketAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
            ticket_attachment = TicketAttachment.query.filter_by(
                ticket_id=ticket_id
            ).all()
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching user and ticket data : {e}"
            )
            raise InternalServerError
        else:
            if not ticket:
                raise NotFoundError(status_msg="Ticket does not exists")
            if not user:
                raise NotFoundError(status_msg="User does not exists")

            if ticket.status == "resolved":
                raise BadRequest(status_msg=f"Resolved tickets can't be edited.")

            role = user.role

            if role == "support" or (
                role == "student" and (user_id == ticket.owner_id)
            ):
                # add attachments now
                status, message = ticket_utils.save_ticket_attachments(
                    attachments, ticket_id, user_id, operation="update_ticket"
                )
            
            if role == "student":
                if ticket.privacy != details["privacy"]:
                    if details["privacy"] == "public":
                        temp_data = details
                        temp_data["ticket_id"] = ticket_id
                        create_ticket.delay(ticket.created_by, temp_data)
                    else:
                        delete_ticket.delay(ticket.created_by, ticket_id)
                if user_id == ticket.owner_id:
                    # student is creator of the ticket
                    if details["title"] == "" or details["tags"] == "":
                        raise BadRequest(
                            status_msg=f"Ticket titleis required"
                        )

                    ticket.title = details["title"]
                    ticket.description = details["description"]
                    ticket.tags = details["tags"]
                    ticket.privacy = details["privacy"]

                    db.session.add(ticket)
                    db.session.commit()

                    raise Success_200(status_msg="Successfully updated a ticket.")

                else:
                    # student has not created this ticket, so only vote can be done
                    ticket_vote = TicketVote.query.filter_by(
                        ticket_id=ticket_id, user_id=user_id
                    ).first()
                    if ticket_vote:
                        # student has already voted
                        raise AlreadyExistError(
                            status_msg="You have already voted this ticket."
                        )
                    else:
                        # ticket upvoted
                        ticket_vote = TicketVote(ticket_id=ticket_id, user_id=user_id)
                        db.session.add(ticket_vote)

                        ticket.votes = ticket.votes + 1
                        db.session.add(ticket)

                        db.session.commit()
                        raise Success_200(status_msg="Successfully upvoted ticket.")
            
            # TODO , move this funtion to different api to make it simpler
            if role == "support":
                sol = details["solution"]
                print(sol)
                print(len(sol))
                print(ticket_utils.is_blank(sol))
                print(ticket.priority)
                if ticket.priority != details['priority'] and ticket_utils.is_blank(sol):
                    temp = ticket.priority
                    ticket.priority = details['priority']
                    
                    db.session.add(ticket)
                    db.session.commit()
                    
                    # send notification to user who created and voted of priority changes
                    try:
                        ticket_votes = TicketVote.query.filter_by(
                            ticket_id=ticket_id
                        ).all()
                        users_voted = [
                            ticket_vote.user_id for ticket_vote in ticket_votes
                        ]
                        users_voted.append(ticket.owner_id)
                        users_email_name = []
                        for user_id_ in users_voted:
                            user_ = Auth.query.filter_by(user_id=user_id_).first()
                            users_email_name.append(
                                {
                                    "email": user_.email,
                                    "username": user_.username,
                                    "ticket_id": ticket_id,
                                }
                            )

                        resp = send_email(
                            to=users_email_name,
                            sub=f"Your ticket's Priority has been changed!",
                            priority=[temp, details['priority']]
                        )
                    except Exception as e:
                        logger.error(
                            f"TicketAPI->send mail : Error occured while sending notification : {e}"
                        )
                    raise Success_200(status_msg="Priority changed!")
                
                elif ticket_utils.is_blank(sol) and ticket.priority == details['priority']:
                    raise BadRequest(status_msg="Solution can not be empty")
                else:
                    solution = Solution(description=sol, resolved_by=get_username(Auth,user_id), resolved_on= int(time.time()))
                    ticket.status = "resolved"
                    # ticket.resolved_by = user_id
                    # ticket.resolved_on = int(time.time())
                    ticket.solution = solution

                    db.session.add(ticket)
                    db.session.commit()

                    # send notification to user who created as well as voted
                    try:
                        _from = user.email
                        ticket_votes = TicketVote.query.filter_by(
                            ticket_id=ticket_id
                        ).all()
                        users_voted = [
                            ticket_vote.user_id for ticket_vote in ticket_votes
                        ]
                        users_voted.append(ticket.owner_id)
                        users_email_name = []
                        for user_id_ in users_voted:
                            user_ = Auth.query.filter_by(user_id=user_id_).first()
                            users_email_name.append(
                                {
                                    "email": user_.email,
                                    "username": user_.username,
                                    "ticket_id": ticket_id,
                                }
                            )

                        resp = send_email(
                            to=users_email_name,
                            _from=_from,
                            sub="Your ticket is resolved",
                            priority=[None, None]
                        )
                    except Exception as e:
                        logger.error(
                            f"TicketAPI->send mail : Error occured while sending notification : {e}"
                        )

                    raise Success_200(status_msg="Successfully resolved a ticket.")

            if role == "admin":
                # admin dont have access
                raise Unauthenticated(
                    status_msg="Admin don't have access to this endpoint."
                )

    @token_required
    @users_required(users=["student"])
    def delete(self, ticket_id=""):
        """
        Usage
        -----
        Delete a single ticket. Only a student who created  a ticket can delete

        Parameters
        ----------
        ticket is and user id

        Returns
        -------


        """
        user_id = request.headers.get('User-Id',"")

        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check if ticket exists and it is created by user_id
        ticket = None
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->delete : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                privacy = ticket.privacy
                user = Auth.query.filter_by(user_id=user_id).first()
                if user_id == ticket.owner_id:
                    # the ticket and its user are matched i hate this code. maybe somecan help me implement a good db model with automatically deletation

                    # delete ticket votes
                    ticket_votes = TicketVote.query.filter_by(ticket_id=ticket_id).all()
                    for ticket_vote in ticket_votes:
                        db.session.delete(ticket_vote)
                    


                    # delete ticket attachments
                    ticket_attachments = TicketAttachment.query.filter_by(
                        ticket_id=ticket_id
                    ).all()
                    for ticket_attachment in ticket_attachments:
                        db.session.delete(ticket_attachment)
                    

                    # delete solution attachments
                    solution_id = ticket.solution_id
                    print(solution_id)
                    sol_attachments = SolutionAttachment.query.filter_by(solution_id = solution_id).all()
                    print(sol_attachments)
                    for sol_attachment in sol_attachments:
                        db.session.delete(sol_attachment)

                    
                    # delete solutions too
                    sols = Solution.query.filter_by(
                        id=ticket.solution_id
                    ).all()
                    for sol in sols:
                        db.session.delete(sol)
                    

                    # delete the ticket
                    db.session.delete(ticket)
                    db.session.commit()

                    if (privacy == "public"):
                        delete_ticket.delay(ticket.created_by, ticket_id)

                    raise Success_200(status_msg="Ticket deleted successfully")
                else:
                    raise PermissionDenied(
                        status_msg="Only a user who created a ticket can delete it."
                    )
            else:
                raise NotFoundError(status_msg="Ticket does not exists")


class AllTicketsAPI(Resource):
    @token_required
    @users_required(users=["student", "support", "admin"])
    def get(self):
        """
        Usage
        -----
        Get all tickets based on query and user role.
        Sorting and filtering will be applied as per query.
        Student needs all tickets while searching and needs all their tickets (created and upvoted)
        Support needs pending tickets while resolving and needs all their resolved tickets
        Admin needs resolved tickets while creating FAQ

        Parameters
        ----------
        query

        Returns
        -------
        List of tickets
        """

        # user is student and is searching tickets while creating a new ticket.
        # get query arguments
        try:
            args = request.args.to_dict(flat=True)
            args = ticket_utils.get_args_from_query(args)
            user_id = request.headers.get("user_id", "")
        except Exception as e:
            logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
            raise InternalServerError
        user = Auth.query.filter_by(
            user_id=user_id
        ).first()  # user already exists as user_required verified it

        # verify if user is student -- Why? what a uselss design
        # if user.role != "student":
        #     raise PermissionDenied(
        #         status_msg="Only student can search all tickets using query."
        #     )

        all_tickets = []

        # get all tickets
        if user.role == "student":
            tickets = Ticket.query.filter_by(privacy="public").all()
            for ticket in tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)
        else:
            tickets = Ticket.query.all()
            for ticket in tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        all_tickets = ticket_utils.tickets_filter_sort(all_tickets, args)

        logger.info(f"All tickets found : {len(all_tickets)}")

        return success_200_custom(data=all_tickets)


class AllTicketsUserAPI(Resource):
    @token_required
    @users_required(users=["student", "support", "admin"])
    def get(self, user_id=""):
        # tickets retrieved based on user role.
        user_id = request.headers.get("User-Id")
        if ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # get query arguments
        try:
            args = request.args.to_dict(flat=True)

            args = ticket_utils.get_args_from_query(args)
        except Exception as e:
            logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
            raise InternalServerError
        user = Auth.query.filter_by(
            user_id=user_id
        ).first()  # user already exists as user_required verified it

        all_tickets = []

        # verify user role
        role = user.role

        if role == "student":
            # student : all tickets created or upvoted by him/her
            # status, priority, sort, filter will be as per filter options received
            # upvoted ticket can be checked by comparing created_by with user_id
            upvoted_ticket_ids = TicketVote.query.filter_by(user_id=user.user_id).all()
            upvoted_ticket_ids = [elem.ticket_id for elem in upvoted_ticket_ids]
            user_tickets = Ticket.query.filter_by(owner_id=user.user_id).all()
            for ticket in user_tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)
            for ticket_id in upvoted_ticket_ids:
                ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        if role == "support":
            # support : all tickets resolvedby him/her
            # get all pending tickets
            # status, priority, sort, filter will be as per filter options received

            if "resolved" in args["status"]:
                # get all tickets resolved by the support staff
                username = get_username(Auth,user.user_id)
                user_tickets = Ticket.query.filter_by(resolved_by=username).all()
            elif "pending" in args["status"]:
                # get all pending tickets
                user_tickets = Ticket.query.filter_by(status="pending").all()
            else:
                user_tickets = []
            for ticket in user_tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        if role == "admin":
            # admin : get all tickets resolved globally (for creating faq)
            # status, priority, sort, filter will be as per filter options received
            user_tickets = Ticket.query.filter_by(status="resolved").all()
            for ticket in user_tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        all_tickets = ticket_utils.tickets_filter_sort(all_tickets, args)
        logger.info(f"All tickets found : {len(all_tickets)}")

        return success_200_custom(data=all_tickets)


class TicketGetPriorityTicketsAPI(Resource):
    @token_required
    @users_required(users=["support", "admin"])
    def get(self,priority):
        priority_tickets = Ticket.query.filter_by(priority=priority, status="pending").all()
        ids = []
        for ticket in priority_tickets:
                ids.append(ticket.ticket_id)
        return success_200_custom(data=ids)


class TicketChangePriorityAPI(Resource):
    @token_required
    @users_required(users=["support", "admin"])
    def post(self):
        request_body = request.get_json()
        ticket_id = request_body['ticket_id']
        priority = request_body['priority'].lower()
        priorities_allowed = ["high", "low", "medium"]
        ticket_obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
        user_id = get_user_id()
        priority_changer_name = get_username(Auth, user_id)
        
        if ticket_obj:
            temp = ticket_obj.priority
            if priority.lower() in priorities_allowed:
                ticket_obj.priority = priority
                db.session.add(ticket_obj)
                db.session.commit()
            else:
                raise BadRequest(status_msg = "Invalid Priority Received")
            
            try:
                ticket_votes = TicketVote.query.filter_by(ticket_id=ticket_id).all()
                users_voted = [ticket_vote.user_id for ticket_vote in ticket_votes]
                users_voted.append(ticket_obj.owner_id)
                users_email_name = []
                for user_id_ in users_voted:
                    user_ = Auth.query.filter_by(user_id=user_id_).first()
                    users_email_name.append(
                        {
                            "email": user_.email,
                            "username": user_.username,
                            "ticket_id": ticket_id,
                        }
                    )
                async_send_email.delay(
                    to=users_email_name,
                    sub=f"Ticket - {ticket_obj.title}'s Priority has been changed!", 
                    priority=[temp, ticket_obj.priority]
                )
                send_gchat_notification(priority_changer_name, ticket_id, ticket_obj.priority)
            except Exception as e:
                print(e)
                pass
        else:
            raise BadRequest(status_msg = "Invalid Ticket Id Received")
        return success_200_custom("Successfuly Changed Priority")

class TicketChangePrivacyAPI(Resource):
    @token_required
    @users_required(users=["student","support", "admin"])
    def put(self):
        request_body = request.get_json()
        ticket_id = request_body['ticket_id']
        privacy = request_body['private']
        ticket_obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
        if ticket_obj:
            ticket_obj.privacy = "private" if privacy else "public"
            db.session.add(ticket_obj)
            db.session.commit()
            ticket_obj = ticket_utils.convert_ticket_to_dict(ticket_obj)
            if privacy:
                pass
            else:
                create_ticket.delay(api_username=ticket_obj.created_by,ticket_obj = ticket_obj)
                if (ticket_obj.solution_id > 0):
                    data = {
                        "description": ticket_obj.solution.description,
                        "ticket_id": ticket_id,
                    }
                    create_reply.delay(ticket_obj.resolved_by, data) #pass resolver name as api-username and data as reply object  

        else:
            raise BadRequest(status_msg = "Invalid Ticket Id Received")
        return success_200_custom("Successfuly Changed Privacy!")

class TicketSolveAPI(Resource):
    @token_required
    @users_required(users=["support", "student", "admin"])
    def post(self):
        request_body = request.get_json()
        ticket_id = request_body['ticket_id']
        ticket_obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
        if ticket_obj:
            ticket_obj.status = "resolved"
            db.session.add(ticket_obj)
            db.session.commit()
            if ticket_obj.privacy == "public":
                try:
                    request_discourse_accept.delay(api_username=ticket_obj.created_by, id=ticket_obj.solution.discourse_id)
                except Exception as e:
                    print(e)
                    pass
            try:
                ticket_votes = TicketVote.query.filter_by(ticket_id=ticket_id).all()
                users_voted = [ticket_vote.user_id for ticket_vote in ticket_votes]
                users_voted.append(ticket_obj.owner_id)
                users_email_name = []
                for user_id_ in users_voted:
                    user_ = Auth.query.filter_by(user_id=user_id_).first()
                    users_email_name.append(
                        {
                            "email": user_.email,
                            "username": user_.username,
                            "ticket_id": ticket_id,
                        }
                    )
                async_send_email.delay(
                    to=users_email_name,
                    sub=f"Ticket -> {ticket_obj.title} is resolved",
                    priority=None
                )
            except:
                pass
        else:
            raise BadRequest(status_msg = "Invalid Ticket Id Received")
        return success_200_custom("Successfuly Marked As Resolved!")


class TicketUnSolveAPI(Resource):
    @token_required
    @users_required(users=["support", "student", "admin"])
    def post(self):
        request_body = request.get_json()
        ticket_id = request_body['ticket_id']
        # user_id = get_user_id()
        # username = get_username(Auth,user_id)
        ticket_obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
        if ticket_obj:
            ticket_obj.status = "pending"
            db.session.add(ticket_obj)
            db.session.commit()
            if ticket_obj.privacy == "public":
                try:
                    request_discourse_unaccept.delay(api_username=ticket_obj.created_by, id=ticket_obj.solution.discourse_id)
                except Exception as e:
                    print(e)
                    pass
            try:
                ticket_votes = TicketVote.query.filter_by(ticket_id=ticket_id).all()
                users_voted = [ticket_vote.user_id for ticket_vote in ticket_votes]
                users_voted.append(ticket_obj.owner_id)
                users_email_name = []
                for user_id_ in users_voted:
                    user_ = Auth.query.filter_by(user_id=user_id_).first()
                    users_email_name.append(
                        {
                            "email": user_.email,
                            "username": user_.username,
                            "ticket_id": ticket_id,
                        }
                    )
                async_send_email.delay(
                    to=users_email_name,
                    sub=f"Ticket -> {ticket_obj.title} is opened again",
                    priority=None
                )
            except:
                pass
        else:
            raise BadRequest(status_msg = "Invalid Ticket Id Received")
        return success_200_custom("Successfuly Marked As Pending!")

class TicketVoteAPI(Resource):
    @token_required
    @users_required(users=["support", "student", "admin"])
    def get(self,ticket_id):
        user_id = get_user_id()
        try:
            ticket_obj = TicketVote.query.filter_by(ticket_id=ticket_id,user_id=user_id).first()
            if ticket_obj:
                return success_200_custom("voted")
            else:
                return success_200_custom("can vote")
        except:
            raise BadRequest(status_msg="No ticket is found")


    @token_required
    @users_required(users=["support", "student", "admin"])
    def post(self):
        request_body = request.get_json()
        user_id = get_user_id()
        ticket_id = request_body['ticket_id']
        ticket_obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
        if ticket_obj.owner_id != user_id :
            try:
                ticket_vote = TicketVote.query.filter_by(ticket_id=ticket_id, user_id=user_id).first()
                ticket_vote_obj = None
                if (ticket_vote is None):
                    ticket_obj.votes = ticket_obj.votes+1
                    ticket_vote_obj = TicketVote(ticket_id=ticket_id, user_id=user_id)
                    db.session.add(ticket_vote_obj)
                    db.session.add(ticket_obj)
                db.session.commit()
            except Exception as e:
                pass
        else:
            raise BadRequest(status_msg = "You can't Vote Your Own Ticket")
        return success_200_custom("Successfuly Voted!")

class TicketReplyAPI(Resource):

    @token_required
    @users_required(users=["support", "admin"])
    def post(self):
        ### Reply to a ticket. can be done by Support and Admins
        request_body = request.get_json()
        ticket_id = request_body.get('ticket_id',"")
        solution = request_body.get('solution',"")
        
        attachments = request_body.get("attachments", [])
        ## getting future last record from solution table because somehow i have to pass that in attachment saver function. 
        ## bad design. i hate working on this codebase
        ticket_obj = Ticket.query.filter_by(ticket_id=ticket_id).first()
        #  modify exsisting support's replies if ticket_obj.solution_id != -1;
        if ticket_obj:
            user_id = get_user_id()
            resolver_name = get_username(Auth,user_id)
            solution_obj = None
            if(ticket_obj.solution_id != -1):
                solution_obj = Solution.query.filter_by(id=ticket_obj.solution_id).first()
            
                # before appending attachments, lets, clear all the attachments in db if the support is not the same
                if (resolver_name != solution_obj.resolved_by):
                    try:
                        db.session.query(SolutionAttachment).filter_by(solution_id=ticket_obj.solution_id).delete()
                        db.session.commit()
                    except Exception:
                        pass
                solution_obj.description = solution
                solution_obj.resolved_on=int(time.time())
                solution_obj.resolved_by=resolver_name
                status, message = ticket_utils.save_solution_attachments(attachments, ticket_obj.solution_id , user_id, operation="update_ticket")
            else:
                last_record = db.session.query(Solution).order_by(Solution.id.desc()).first()
                last_record_id = last_record.id if last_record else 0
                last_record_id+=1
                status, message = ticket_utils.save_solution_attachments(attachments, last_record_id, user_id, operation="update_ticket")
                solution_obj = Solution(description=solution, resolved_by=resolver_name,resolved_on=int(time.time()))
                ticket_obj.solution_id = last_record_id

            db.session.add(ticket_obj)
            db.session.add(solution_obj)
            db.session.commit()
            if ticket_obj.privacy == 'public':
                data = {
                    "description": solution,
                    "ticket_id": ticket_id,
                }
                create_reply.delay(resolver_name,data) #pass the repliers username and the reply body
            try:
                ticket_votes = TicketVote.query.filter_by(ticket_id=ticket_id).all()
                users_voted = [ticket_vote.user_id for ticket_vote in ticket_votes]
                users_voted.append(ticket_obj.owner_id)
                users_email_name = []
                for user_id_ in users_voted:
                    user_ = Auth.query.filter_by(user_id=user_id_).first()
                    users_email_name.append(
                        {
                            "email": user_.email,
                            "username": user_.username,
                            "ticket_id": ticket_id,
                        }
                    )

                async_send_email.delay(
                    to=users_email_name,
                    sub=f"{resolver_name} replied to the ticket -> {ticket_obj.title}",
                    priority=None
                )
            except:
                pass

        #TODO: maybe we can send some notification
        else:
            raise BadRequest(status_msg = "Invalid Ticket Id Received")
        return success_200_custom("Successfuly Replied !")



    
class Ticketsforhome(Resource):
    def get(self):
        all_tkt = []
        # get query arguments
        args = None
        try:
            args = request.args.to_dict(flat=True)
            args = ticket_utils.get_args_from_query(args)
        except Exception as e:
            logger.error(f"Ticketsforhome->get : Error occured while resolving query : {e}")
            raise InternalServerError

        tickets = Ticket.query.filter_by(privacy="public").order_by(Ticket.votes).all()
        #print(tickets)
        for ticket in tickets:
            tkt_detail = ticket_utils.convert_ticket_to_dict(ticket)

            all_tkt.append(tkt_detail)

        all_tickets = ticket_utils.tickets_filter_sort(all_tkt, args)
        return success_200_custom(data=all_tickets)
    
class OnlyViewTicket(Resource):
    def get(self, ticket_id):
        ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        tkt_detail = ticket_utils.convert_ticket_to_dict(ticket)
        return success_200_custom(data=tkt_detail)

class TicketTagsApi(Resource):
    @token_required
    def get(self):
        ###
        # usage - Get all tags
        ###
        tags = []
        try:
            all_tags = db.session.query(Tags).all()
            
            tags = [tag.tag_name for tag in all_tags]
        except:
            raise InternalServerError
        return success_200_custom(data=tags)
    
    @token_required
    @admin_required
    def post(self):
        ###
        # Usage - Creates a new tag
        ###
        data = request.get_json().get("tags",[])
        _all_tags = db.session.query(Tags).all()
        all_tags = [tag.tag_name for tag in _all_tags]
        try:
            for tag in data:
                tag_name = str(tag).upper()
                if tag_name not in all_tags:
                    try:
                        new_tag = Tags(tag_name = tag_name)
                        db.session.add(new_tag)
                        db.session.commit()
                    except Exception as e:
                        print(e)
            return success_200_custom("Tags created successfully")
        except Exception as e:
            raise NotFoundError(status_msg="could not create")
        
    @token_required
    @users_required(users=["admin"])
    def delete(self):
        ###
        # Usage - deletes an existing tag
        ###
        data = request.get_json().get("tag","")
        tag = Tags.query.filter_by(tag_name=str(data).upper()).first()
        if tag:
            db.session.delete(tag)
            db.session.commit()
            raise Success_200(status_msg="Tags deleted successfully")
        else:
            raise NotFoundError(status_msg="No tag can be found to delete")

ticket_api.add_resource(
    TicketAPI,
    "/<string:ticket_id>",
    "/create",
)  # path is /api/v1/ticket
ticket_api.add_resource(AllTicketsAPI, "/all-tickets")
ticket_api.add_resource(AllTicketsUserAPI, "/all-tickets/user")
ticket_api.add_resource(Ticketsforhome, "/few-tickets")
ticket_api.add_resource(OnlyViewTicket, "/onlyview/<string:ticket_id>")
ticket_api.add_resource(TicketTagsApi, "/tags")
ticket_api.add_resource(TicketVoteAPI,"/vote/<string:ticket_id>", "/vote")

ticket_api.add_resource(TicketGetPriorityTicketsAPI, "/priority/<string:priority>")
ticket_api.add_resource(TicketChangePrivacyAPI, "/change/privacy")
ticket_api.add_resource(TicketChangePriorityAPI, "/change/priority")
ticket_api.add_resource(TicketSolveAPI, "/solve")
ticket_api.add_resource(TicketUnSolveAPI, "/unsolve")
ticket_api.add_resource(TicketReplyAPI, "/reply")


# --------------------  END  --------------------
