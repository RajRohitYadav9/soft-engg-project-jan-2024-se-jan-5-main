# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains global constants and variables.

# --------------------  Imports  --------------------

import os
from dotenv import load_dotenv

# --------------------  Code  --------------------
# Load environment variables from .env file (assuming it's in the same directory)
load_dotenv()
BACKEND_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
HOST = "127.0.0.1"
PORT = 5000
DISCOURSE_PORT = 3000
DISCOURSE_API_KEY = os.getenv('API_KEY')
DISCOURSE_ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
GMAIL_SENDER = os.getenv('GMAIL_SENDER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
DEBUG = True
ENV_TYPE = "dev"  # "test"
BASE = f"http://{HOST}:{PORT}"
DISCOURSE_BASE_URL = f"http://{HOST}:{DISCOURSE_PORT}/"
API_VERSION = "v1"
TOKEN_VALIDITY = 60000  # seconds
ACCEPTED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]
PROFILE_PIC_PATH = os.path.join(
    BACKEND_ROOT_PATH, "databases", "images", "profile_pics"
)
TICKET_ATTACHMENTS_PATH = os.path.join(
    BACKEND_ROOT_PATH, "databases", "images", "ticket_attachments"
)
FAQ_ATTACHMENTS_PATH = os.path.join(
    BACKEND_ROOT_PATH, "databases", "images", "faq_attachments"
)

# Mailhog runs at http://127.0.0.1:8025/
SMTP_SERVER_HOST = "127.0.0.1"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "osts_group_14@gmail.com"  # dummy mail and password
SENDER_PASSWORD = "1234"

# --------------------  END  --------------------
