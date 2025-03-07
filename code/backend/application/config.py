# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This file contains app configuration.

# --------------------  Imports  --------------------

from .globals import BACKEND_ROOT_PATH
import os
from sqlalchemy.pool import QueuePool
# --------------------  Code  --------------------


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    db_path = os.path.join(
        BACKEND_ROOT_PATH, "databases", "supportTicketDB_Prod.sqlite3"
    )
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path + "?charset=utf8"
    SECRET_KEY = "secretKey"
    DEBUG = False


class TestingConfig(Config):
    db_path = os.path.join(
        BACKEND_ROOT_PATH, "databases", "supportTicketDB_Test.sqlite3"
    )
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path + "?charset=utf8"
    SECRET_KEY = "secretKey"
    DEBUG = True


class DevelopmentConfig(Config):
    db_path = os.path.join(
        BACKEND_ROOT_PATH, "databases", "supportTicketDB_Dev.sqlite3"
    )
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path + "?charset=utf8"
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': QueuePool,
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True
    }
    # SQLALCHEMY_ECHO = True # for sqlalchemy debug queries
    SECRET_KEY = "secretKey"
    DEBUG = True


# --------------------  END  --------------------
