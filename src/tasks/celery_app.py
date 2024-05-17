__all__ = ["celery_app"]

from celery import Celery
from sqlalchemy_celery_beat.schedulers import DatabaseScheduler
from loguru import logger

# import os, sys
# sys.path.append(os.getcwd() + r"\src")
# sys.path.insert(1, os.getcwd() + r"\src")

from config import settings



class CeleryConfig:
    include = ["tasks.service"]
    result_expires = 3600
    timezone = settings.TIMEZONE
    broker_url = settings.REDIS_URL
    # result_backend = settings.REDIS_URL
    result_backend = 'db+sqlite:///results.db'
    beat_dburi = settings.BEAT_DBURL
    beat_schema = None
    beat_scheduler = DatabaseScheduler
    # worker_pool_restarts = True

celery_app = Celery('tasks')
celery_app.config_from_object(CeleryConfig)


