# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains notifications methods to send mail to users.

# --------------------  Imports  --------------------

from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify
from .logger import logger
from jinja2 import Template
from flask import render_template, request, redirect, flash, url_for
import pandas as pd
import requests
from datetime import datetime
import os
import json
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
from email.mime.application import MIMEApplication
from .globals import *
import ssl


# --------------------  Code  --------------------


notification_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Alert</title>
</head>
<body>
    <p>Dear {{ data['username'] }},</p>
    <p>&emsp;Your ticket with ticket ID :<b>{{ data['ticket_id'] }}</b> has been resolved by support team member.</p>
    <p>&emsp;Please login to your acccount and verify the solution.</p>
    </br>
    <p>Regards,</p>
    <p>OSTS Support Team</p>
</body>
</html>
"""

notification_template_priority = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Alert</title>
</head>
<body>
    <p>Dear {{ data['username'] }},</p>
    <p>&emsp;The priority of your ticket with ticket ID :<b>{{ data['ticket_id'] }}</b> has been changed from <b>{{ data['priority'][0] }}</b> to <b>{{ data['priority'][1] }}</b> by support team member.</p>
    <p>&emsp;Please login to your acccount and verify.</p>
    </br>
    <p>Regards,</p>
    <p>OSTS Support Team</p>
</body>
</html>
"""

def render_forgot_password_template(password):
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Alert</title>
    </head>
    <html>
    <body>
        <p>Dear user,</p>
        <p>Your new password for OSTS is: {password}</p>
        <p>Please use this password to log in to the OSTS system.</p>
        <p>Thank you,</p>
        <p>The OSTS Team</p>
    </body>
    </html>
    """
    return template

def check_internet():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        return False

smtp_port = 587
smtp_server = "smtp.gmail.com"


import smtplib
from email.mime.multipart import MIMEMultipart


def render_template(data,priority=None):
    if priority is None:
        notification_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Alert</title>
        </head>
        <body>
            <p>Dear { data['username'] },</p>
            <p>&emsp;Your ticket with ticket ID :<b>{ data['ticket_id'] }</b> has been resolved by support team member.</p>
            <p>&emsp;Please login to your acccount and verify the solution. </p><a href='http://localhost:8080'>OSTS</a>
            </br>
            <p>Regards,</p>
            <p>OSTS Support Team</p>
        </body>
        </html>
        """
    else:
        notification_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Alert</title>
        </head>
        <body>
            <p>Dear { data['username'] },</p>
            <p>&emsp;The priority of your ticket with ticket ID :<b>{ data['ticket_id'] }</b> has been changed from <b>{ priority[0] }</b> to <b>{ priority[1] }</b> by support team member.</p>
            <p>&emsp;Please login to your acccount and verify.</p>
            <a href='http://localhost:8080'>OSTS</a>
            </br>
            <p>Regards,</p>
            <p>OSTS Support Team</p>
        </body>
        </html>
        """
    return notification_template


def _send_mail(to, _from,subject, priority, content="html"):
    email_from = GMAIL_SENDER #senders email
    users = to

    pswd = GMAIL_PASSWORD #app key generated using actual gmail id of sender
    
    if(priority != None):
        print("Priority")
    else:
        print("Not priority")

  # Use smtplib with STARTTLS for TLS connection
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_from, pswd)
        data = None
        try:
            for user in users:
                data={"username": user["username"], "ticket_id": user["ticket_id"]}
                msg = MIMEMultipart()
                msg['From'] = email_from
                email_to = user["email"]
                msg['To'] = email_to
                msg['Subject'] = subject
                msg_template = render_template(data, priority)
                msg.attach(MIMEText(msg_template, 'html'))
                server.sendmail(email_from, email_to, msg.as_string())
        except Exception as e:
            return e

    return "Email sent successfully!"


def send_email(to=[],_from="",sub="",priority = None):
    return _send_mail(
                to=to,
                _from="",
                subject=sub,
                priority=priority,
                content="html",
            )
    return "failed to send gmail"


def send_forgot_password_email(to,password):
    email_from = GMAIL_SENDER #senders email
    pswd = GMAIL_PASSWORD #app key generated using actual gmail id of sender

  # Use smtplib with STARTTLS for TLS connection
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_from, pswd)
        data = None
        try:
            msg = MIMEMultipart()
            msg['From'] = email_from
            email_to = to
            msg['To'] = email_to
            msg['Subject'] = "Your New Password For OSTS !"
            msg_template = render_forgot_password_template(password)
            msg.attach(MIMEText(msg_template, 'html'))
            server.sendmail(email_from, email_to, msg.as_string())
        except Exception as e:
            return 400
    return 200
    
# --------------------  END  ------------------
