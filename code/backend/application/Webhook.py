from json import dumps
from httplib2 import Http
from celery.schedules import crontab

from datetime import datetime



def google_chatroom_notification(support_name, ticket_id, priority):

    def make_api_request():
        # Make the API request
        message = f"Support - {support_name} channged the priority of ticket with id - {ticket_id} to {priority}\nLogin or go to - http://localhost:8080/ticket/{ticket_id} to solve the issue ASAP!"
        url = "https://chat.googleapis.com/v1/spaces/AAAAYJfSwPI/messages?key=AIzaI&token=T"
        app_message = {"text": message}
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        try:
            response = http_obj.request(
                uri = url,
                method = "POST",
                headers = message_headers,
                body = dumps(app_message),
            )
            return 200
        except Exception as e:
            print(e)
            return e
    try:
        # Attempt to make the API request
        return make_api_request()
    except RequestException:
        # If there's a RequestException (e.g., no internet connection), attempt to establish a new connection
        session = requests.Session()
        session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
        session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))

        try:
            # Try to make the API request again with the new session
            return make_api_request()
        except RequestException as e:
            return f"Error: {e}"


import requests
from requests.exceptions import RequestException

def google_chatroom(ticket_count, last24count):
    def make_api_request():
        # Make the API request
        message = f"Hello Instructors!\nTotal number of unresolved High priority tickets: {ticket_count}\nTotal number of new tickets in the last 24 hours: {last24count}"
        url = "https://chat.googleapis.com/v1/spaces/AAAAYJfSwPI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=TdwPamtmsKDY0NanD76qFQo6CUHGsBmtyfVuztP41FE"
        app_message = {"text": message}
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}

        try:
            response = requests.post(url, json=app_message, headers=message_headers)
            if response.status_code == 200:
                return "Success"
            else:
                return f"Error: {response.status_code}"
        except RequestException as e:
            return f"Error: {e}"

    try:
        # Attempt to make the API request
        return make_api_request()
    except RequestException:
        # If there's a RequestException (e.g., no internet connection), attempt to establish a new connection
        session = requests.Session()
        session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
        session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))

        try:
            # Try to make the API request again with the new session
            return make_api_request()
        except RequestException as e:
            return f"Error: {e}"
