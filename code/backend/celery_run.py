from celery import Celery
from .celery.tasks import celery

if __name__ == '__main__':
    celery.worker_main()