# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is main app file where backend application starts.

# --------------------  Imports  --------------------

from flask import Flask
from application.config import DevelopmentConfig, TestingConfig
from application.models import db, Tags, Auth
from application.logger import logger
from application.globals import API_VERSION
from application.views.auth_bp import auth_bp
from application.views.student_bp import student_bp
from application.views.support_bp import support_bp
from application.views.admin_bp import admin_bp
from application.views.faq_bp import faq_bp
from application.views.ticket_bp import ticket_bp
from application.views.user_bp import user_bp
from application.views.forgot_password_bp import forgot_password_bp
from application import cache
from flask_cors import CORS

from application.common_utils import hash_password


# from application import create_app
from application.globals import HOST, PORT, DEBUG, ENV_TYPE
from celery import Celery
from application.tasks import send_reminder
from application import tasks
from celery.schedules import crontab

# --------------------  Initialization  --------------------


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
    app.register_blueprint(user_bp, url_prefix=f"/api/{API_VERSION}/user")
    app.register_blueprint(forgot_password_bp, url_prefix=f"/api/{API_VERSION}/password")

    cache.init_app(app)

    app.app_context().push()
    db.create_all()


    try:
        # prefill tags
        # create Admin Tags
        db.session.add(Tags(id=1,tag_name="GENERAL"))
        admin = Auth(
            user_id  = 1,
            name="Admin", username="admin",
            password=hash_password("12345678"),
            email="admin@gmail.com",
            role="admin",
            is_verified=True)
        db.session.add(admin)
        db.session.commit()
    except:
        pass

    return app


app = create_app(env_type=ENV_TYPE)

# celery = Celery('Application jobs',broker='pyamqp://guest:guest@localhost:5672//')

# celery.Task = workers.ContextTask
# celery.conf.update(app.config)



# @celery.on_after_finalize.connect
# def Daily_Reminder(sender, **kwargs):
#     sender.add_periodic_task(crontab(minute=1),send_reminder.s(),name="send notification daily")
# --------------------  Main  --------------------
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)

# --------------------  End  --------------------
