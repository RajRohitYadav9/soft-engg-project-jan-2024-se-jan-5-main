from backend.application.tasks import create_user, create_ticket, create_reply
import pytest

from backend.application import db
from backend.application.models import Auth
from backend.application.globals import *


def test_discourse_create_user():
    data = {
        "name": "exampl3e.com",
        "email": "example@12334.gmail.com",
        "unhashed_password" : "password13234",
        "username": "exampleTesterTY"
    }
    res = create_user(api_key = DISCOURSE_API_KEY, api_username = "xyzporag0000", user_obj = data)
    assert res == 200

def test_discourse_create_ticket():
    data = {
        "title": "example.com is uyhu the title",
        "description": "this is iuji testing description",
        "ticket_id" : "1000132dc",
    }
    res = create_ticket(api_key = DISCOURSE_API_KEY, api_username = "xyzporag0000", ticket_obj = data)
    assert res == 200

def test_discourse_reply():
    data = {
        "description": "this is testiuung description",
        "ticket_id" : "1000132dc",
    }
    res = create_reply(api_key=DISCOURSE_API_KEY,api_username="xyzporag0000",ticket_obj=data)
    assert res == 200

def test_delete_discourse_account():
    pass

def test_mark_topic_solve_discourse():
    pass