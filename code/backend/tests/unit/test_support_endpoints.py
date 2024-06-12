import pytest

from backend.application import db
from backend.application.models import Auth
from backend.application.globals import *


headers = {
    "Content-type": "application/json",
    "Web-Token": "",
    "User-Id": "",
}


# Support Register and Login------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------v
def test_support_register_success(test_client):
    # Send a POST request with valid registration data
    response = test_client.post(f"/api/{API_VERSION}/auth/register", json={"email": "new_supportr@domain.com", "password": "password123","retype_password":"password123","role":"support", "name":"TestSupport","username":"TestSupport","is_verified":True},headers=headers)
    assert response.status_code == 200



def test_support_login_success(test_client):
    # Send a POST request with correct credentials
    response = test_client.post(f"/api/{API_VERSION}/auth/login", json={"username": "TestSupport", "password": "password123"},)
    assert response.status_code == 200

    headers["Web-Token"] = response.json["message"]["web_token"]
    headers["User-Id"] = response.json["message"]["user_id"]
    assert headers["User-Id"] != ""
    assert headers["Web-Token"] != ""
    

# Test Reply Functionality--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

#/api/v1/ticket/reply
def test_reply_to_ticket(test_client):
    data = {
        "ticket_id": 3,
        "solution": "This is the Test Solution",
        "attachments": [], 
    }
    response = test_client.post(f"/api/{API_VERSION}/ticket/reply", json=data, headers=headers)
    assert response.get_json()["status"] == 200