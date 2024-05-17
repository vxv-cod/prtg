
import asyncio
import os
from celery import Celery
from celery.schedules import crontab

# import nest_asyncio
# nest_asyncio.apply()

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone

from loguru import logger
import pytz

from test.test_tasks.custom_scheduler import CustomScheduler




celery_app = Celery(
    __name__,
    broker = 'redis://localhost:6379',
    backend = 'redis://localhost:6379',
    include=["tasks.tasks_service"]
)

# celery_app.conf.beat_schedule = {}
# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=600,
    timezone='Asia/Yekaterinburg',

)

celery_app.conf.beat_scheduler = CustomScheduler

# celery_app.conf.timezone = 'Europe/London'
# celery_app.config_from_object()


# celery_app.conf.enable_utc = False




# celery_app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     # '"Задача по будням данных за вчерашние сутки"': {
#     '"add_every_seconds"': {
#         'task': 'tasks.tasks_service.add_task_sync',
#         # 'schedule': crontab(hour=16, minute=31, day_of_week=1),
#         'schedule': 10.0,
#         # 'schedule': timedelta(seconds=5),
#         # 'schedule': crontab(hour = 17, minute = 7, day_of_week="2,3,4,5,6"),
#         'args': [datetime.now().date() - timedelta(days=1)],
#         'kwargs': {"hours" : 1, "stime" : "08-00-00", "etime" : "18-00-00"}
#     },
# }


if __name__ == "__main__":
    celery_app.start([
        "beat", 
        # "-S celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler", 
        # "-l info", 
        # "-s logs_celerybeat/celerybeat-schedule", 
        # r"-s logs_celerybeat\celerybeat-schedule.dat",
        "--loglevel=info"
    ])