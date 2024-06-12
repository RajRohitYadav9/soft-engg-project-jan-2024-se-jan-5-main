import pytest

from backend.application import db
from backend.application.models import Auth
from backend.application.globals import *


headers = {
    "Content-type": "application/json",
    "Web-Token": "",
    "User-Id": "",
}
def test_register_success(test_client):
    # Send a POST request with valid registration data
    response = test_client.post(f"/api/{API_VERSION}/auth/register", json={"email": "new_user@example.com", "password": "password123","retype_password":"password123","role":"student", "name":"Parag","username":"Parag123","is_verified":True},headers=headers)
    assert response.status_code == 200


def test_student_login_success(test_client):
    # Send a POST request with correct credentials
    response = test_client.post(f"/api/{API_VERSION}/auth/login", json={"username": "Parag123", "password": "password123"},)
    assert response.status_code == 200

    headers["Web-Token"] = response.json["message"]["web_token"]
    headers["User-Id"] = response.json["message"]["user_id"]
    assert headers["User-Id"] != ""
    assert headers["Web-Token"] != ""


def test_login_invalid_credentials(test_client):
    # Send a POST request with invalid email
    response = test_client.post(f"/api/{API_VERSION}/auth/login", json={"email": "invalid@example.com", "password": "password"})
    assert response.status_code == 404
    assert response.json['message'] == 'User does not exists'


def test_register_duplicate_email(test_client):

    # Try to register with the same email
    response = test_client.post(f"/api/{API_VERSION}/auth/register", json={"email": "new_user@example.com", "password": "password123","retype_password":"password123","role":"student", "name":"Parag","username":"Parag123","is_verified":True})

    assert response.status_code == 409
    assert response.json['message'] == 'Email is already in use'

def test_student_creates_new_ticket(test_client):
    # Create a new Ticket
    ticket_details = {
            "title": "this is test ticket",
            "description": "this is test description",
            "tags": "general,oppe", # get all tags as string seperated by commas
            "privacy": "public", # "public or private"
        }
    response = test_client.post(f"/api/{API_VERSION}/ticket/create",json=ticket_details,headers=headers)
    print(response)
    assert response.status_code == 200

def test_student_gets_all_pending_tickets(test_client):
    # Searches all tickets created by himself or other students
    response = test_client.get(
    f"/api/{API_VERSION}/ticket/all-tickets?filter_priority=&filter_status=pending&sortby=&sortdir=&filter_tags=",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert type(response["message"]) == list
    if response["message"]:
        status = [i["status"] for i in response["message"]]
        assert "resolved" not in status
    pass

def test_student_gets_all_resolved_tickets(test_client):
    # Searches all tickets created by himself or other students
    response = test_client.get(
    f"/api/{API_VERSION}/ticket/all-tickets?filter_priority=&filter_status=resolved&sortby=&sortdir=&filter_tags=",
        headers=headers,
    )
    response = response.get_json()
    assert response["status"] == 200
    assert type(response["message"]) == list
    if response["message"]:
        status = [i["status"] for i in response["message"]]
        assert "pending" not in status
    pass

def test_student_edits_ticket(test_client):
     # Edit a ticket
     pass

def test_student_deletes_ticket(test_client):
    # Delets a ticket
    pass

def test_student_upvotes_ticket(test_client):
    # Upvotes a ticket
    pass
    