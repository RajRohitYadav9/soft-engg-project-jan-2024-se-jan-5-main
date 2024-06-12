
from flask import current_app as app
from celery import Celery
from .tasks import *
from .globals import DISCOURSE_BASE_URL, BACKEND_ROOT_PATH, DISCOURSE_API_KEY, DISCOURSE_ADMIN_USERNAME
from requests import request
from celery.schedules import crontab
from celery import Celery
from .Webhook import google_chatroom

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from .models import Ticket, Solution
import time
from datetime import datetime, timedelta
import os
from .notifications import send_email, send_forgot_password_email
from .Webhook import  google_chatroom_notification, google_chatroom
from json import dumps
from httplib2 import Http




celery = Celery('Application jobs',broker='pyamqp://guest:guest@localhost:5672//')

# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

#2.-Turn on database engine
# ensure this is the correct path for the sqlite file. 
db_path = os.path.join(
    BACKEND_ROOT_PATH, "databases", "supportTicketDB_Dev.sqlite3"
)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path + "?charset=utf8"
db_engine=sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={'check_same_thread': False},
    pool_pre_ping=True,
    pool_size=5,
    poolclass=QueuePool
)
Session = sessionmaker(db_engine)
db_session = Session()

# celery.Task = ContextTask

@celery.on_after_finalize.connect
def Daily_Reminder(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0,minute=0),send_reminder.s(),name="send notification daily")
    # sender.add_periodic_task(1 * 60, send_reminder.s(), name="send notification every 5 minutes")


@celery.task(name="create_ticket",priority=1)
def create_ticket(api_username, ticket_obj):
    title = _get_title(ticket_obj)
    description = _get_description(ticket_obj)
    external_id = _get_external_id(ticket_obj)
    data = {
        "title" : title,
        "raw" : description,
        "external_id" : external_id,
        "category": 4,
    }
    res = request(method="POST", url = _get_url("posts.json"), json = data, headers=_get_header(api_username))
    print(res.text)
    return "success"

@celery.task(name="delete_user")
def delete_user(username):

    headers = _get_header()
    #first get user by username to get the id
    user_url = _get_url(f"u/{username}.json")
    user = request(method="GET", url=user_url, headers=headers)
    try:
        user_dict = user.json()
        user_id = user_dict["user"]["id"]

        data = {
            "delete_posts": True,
            "block_email": False,
            "block_urls": False,
            "block_ip": False
        }
        
        delete_url = _get_url(f"admin/users/{user_id}.json")
        req = request(method="DELETE", url=delete_url, json=data, headers=headers)
        print(req.text)
        
        if(req.status_code == 200):
            return f"successfully deleted - {username}"
        else:
            return f"Failed to delete - {username}"
    except Exception as e:
        print(e)
        return f"Failed to delete - {username}"


@celery.task(name="async_send_email")
def async_send_email(to,sub,priority):
    # print(to)
    res = send_email(to=to,sub=sub,priority=priority)
    return res


@celery.task(name="create_reply")
def create_reply(api_username,ticket_obj):
    description = _get_description(ticket_obj)
    external_id = _get_external_id(ticket_obj)
    headers = _get_header(api_username=api_username)
    # get the ticket by external id
    ticket_url = _get_url(f"t/external_id/{external_id}.json")
    ticket = request(method = "GET", url=ticket_url, headers=headers)

    try:
        res_dict = ticket.json()
        topic_id = res_dict["post_stream"]["posts"][0]["topic_id"]
        data = {
            "raw" : description,
            "topic_id" : topic_id,
        }
        res = request(method="POST", url = _get_url("posts.json"), json = data, headers=headers)
        if(res.status_code == 200):
            discourse_id = res.json()["id"]
            ticket = db_session.query(Ticket).filter_by(ticket_id=external_id).first()
            ticket.solution.discourse_id = discourse_id
            db_session.add(ticket)
            db_session.commit()
    except Exception as e:
        print(e)
    return "success"


@celery.task(name="request_discourse_accept")
def request_discourse_accept(api_username, id):
    headers = _get_header(api_username=api_username)
    body={
        'id': id 
    }
    url = _get_url("solution/accept")
    response = request(method="POST", url = url, headers=headers, json=body)
    return response.status_code 


@celery.task(name="request_discourse_unaccept")
def request_discourse_unaccept(api_username, id):
    headers = _get_header(api_username=api_username)
    body={
        'id': id 
    }
    url = _get_url("solution/unaccept")

    response = request(method="POST", url = url, headers=headers, json=body)
    return response.status_code 

@celery.task(name="delete_ticket")
def delete_ticket(api_username,id):
    external_id = id
    headers = _get_header(api_username=api_username)
    # get the ticket by external id
    ticket_url = _get_url(f"t/external_id/{external_id}.json")
    ticket = request(method = "GET", url=ticket_url, headers=headers)
    try:
        res_dict = ticket.json()
        id = res_dict["post_stream"]["posts"][0]["topic_id"]
        url = _get_url(f"t/{id}")
        response = request(method="DELETE", url = url, headers=headers)
        return "success"
    except:
        return "failed to delete ticket from discourse"

    

@celery.task(name="mark_solved")
def mark_solved(resolver_name, discourse_post_id):
    pass

def _get_title(ticket_obj):
    return ticket_obj["title"]
def _get_description(ticket_obj):
    return ticket_obj["description"]
def _get_external_id(ticket_obj):
    return ticket_obj["ticket_id"]

def _get_url(path):
    return DISCOURSE_BASE_URL + path

def _get_header(api_username=DISCOURSE_ADMIN_USERNAME):
    header = ({
            'Api-Key': DISCOURSE_API_KEY,
            'Api-Username': api_username,
            'Content-Type': 'application/json'
    })
    return header

@celery.task(name="create_user")
def create_user(user_obj):
    data = {
        "name": user_obj["name"],
        "email": user_obj["email"],
        "password": user_obj["unhashed_password"],
        "username": user_obj["username"],
        "approved" : True,
        "active" : True,
    }
        # try:
    url = _get_url("users.json")
    header = _get_header()
    res = request(method="POST", url = url, json = data, headers=header)
    print(res.text)
    return "success"


@celery.task(name="async_send_forgot_password_email")
def async_send_forgot_password_email(to, password):
    res = send_forgot_password_email(to,password)
    return res



@celery.task()
def send_reminder():
    all_tickets = db_session.query(Ticket).filter_by(priority = "high", status = "pending").all()
    last24hours = 0
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    if all_tickets:
        for ticket in all_tickets:
            ticket_time = datetime.fromtimestamp(ticket.created_on)
            if(ticket_time >= twenty_four_hours_ago):
                last24hours+=1
    return google_chatroom(len(all_tickets), last24hours)


@celery.task(name="send_gchat_notification")
def send_gchat_notification(support_name, ticket_id, priority):
    res = google_chatroom_notification(support_name, ticket_id, priority)
    return res

