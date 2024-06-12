# Online Support Ticket
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is init file for local package ''.

# --------------------  Imports  --------------------

from flask_caching import Cache

from flask import Flask
from .config import DevelopmentConfig, TestingConfig
from .models import db
from .logger import logger
from .globals import API_VERSION
from .views.auth_bp import auth_bp
from .views.student_bp import student_bp
from .views.support_bp import support_bp
from .views.admin_bp import admin_bp
from .views.faq_bp import faq_bp
from .views.ticket_bp import ticket_bp
from flask_cors import CORS

def create_app(env_type="dev"):
    app = Flask(__name__, template_folder="templates")
    if env_type == "dev":
        app.config.from_object(DevelopmentConfig)
        logger.info("Development environment configured.")
    if env_type == "test":
        app.config.from_object(TestingConfig)
        logger.info("Testing environment configured.")

    db.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(auth_bp, url_prefix=f"/api/{API_VERSION}/auth")
    app.register_blueprint(student_bp, url_prefix=f"/api/{API_VERSION}/student")
    app.register_blueprint(support_bp, url_prefix=f"/api/{API_VERSION}/support")
    app.register_blueprint(admin_bp, url_prefix=f"/api/{API_VERSION}/admin")
    app.register_blueprint(ticket_bp, url_prefix=f"/api/{API_VERSION}/ticket")
    app.register_blueprint(faq_bp, url_prefix=f"/api/{API_VERSION}/faq")

    app.app_context().push()
    db.create_all()
    db.session.commit()

    return app

cache = Cache(config={'CACHE_TYPE': 'simple'})


# --------------------  END  --------------------
