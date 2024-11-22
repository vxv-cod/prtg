__all__ = ["celery_app"]

import datetime
from celery import Celery
from celery.schedules import crontab
from sqlalchemy_celery_beat.schedulers import DatabaseScheduler
from loguru import logger

from config import settings


celery_app = Celery('tasks')

class DatabaseScheduler(DatabaseScheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sync(self):
        try:
            return super().sync()
        except AttributeError:
            print("Отмена сохранения в ДБ --------- AttributeError ---------")
            

class CeleryConfig:
    include = [
        "tasks.tasks_repo",
        "prtg.prtg_service"
    ]
    result_expires = 3600
    timezone = settings.TIMEZONE
    broker_url = settings.REDIS_URL
    beat_dburi = settings.BEAT_DBURL
    # result_backend = settings.BEAT_RESULT
    result_backend = settings.REDIS_URL
    beat_schema = None
    beat_scheduler = DatabaseScheduler
    worker_pool_restarts = True

celery_app.config_from_object(CeleryConfig)



auto_import_histor_kwargs = dict(hours=1, stime="08-00-00", etime="18-00-00")
crontab_schedule = crontab(**dict(hour = 1, minute = "0", day_of_week = "*"))
# schedule = 3
schedule = crontab_schedule

'''1ый вариант'''
celery_app.conf.beat_schedule = {
    'crontab_default': {
        'task': 'tasks.tasks_repo.auto_import_histor',
        'schedule': schedule,
        'kwargs': {**auto_import_histor_kwargs}
    },
}

'''2ой вариант'''
# from tasks.tasks_repo import TasksRepository
# celery_app.add_periodic_task(
#     # schedule = crontab(hour = 1, minute = "0", day_of_week = "*"), 
#     schedule = 5, 
#     sig = TasksRepository.auto_import_histor, 
#     # args = ["every_day"], 
#     kwargs = {**auto_import_histor_kwargs}, 
#     name = 'crontab_auto_import_histor'
# )








# class CeleryConfig:
#     include = ["tasks.service"]
#     # include = ["tasks.celery_tasks"]
#     # include = [celery_tasks]
#     result_expires = 3600
#     timezone = settings.TIMEZONE
#     broker_url = settings.REDIS_URL
#     beat_dburi = settings.BEAT_DBURL
#     result_backend = settings.BEAT_RESULT
#     # result_backend = settings.REDIS_URL
#     beat_schema = None
#     beat_scheduler = DatabaseScheduler
#     worker_pool_restarts = True

    # def sync(self):
    #     """override"""
    #     logger.debug('Writing entries...')
    #     _tried = set()
    #     _failed = set()
    #     try:
    #         while self._dirty:
    #             name = self._dirty.pop()
    #             logger.debug(f"{name = }")
    #             try:
    #                 self.schedule[name].save()  # save to database
    #                 logger.debug(
    #                     '{name} save to database'.format(name=name))
    #                 _tried.add(name)
    #             except (KeyError) as exc:
    #                 logger.debug(f"{exc = }")
    #                 logger.error(exc)
    #                 _failed.add(name)
    #     except sa.exc.DatabaseError as exc:
    #         logger.exception('Database error while sync: %r', exc)
    #     except sa.exc.InterfaceError as exc:
    #         logger.warning(
    #             'DatabaseScheduler: InterfaceError in sync(), '
    #             'waiting to retry in next call...'
    #         )
        
    #     except AttributeError:
    #         print("Ошибка --------- AttributeError ---------")
    #         del self.schedule[name]
        
    #     finally:
    #         # retry later, only for the failed ones
    #         self._dirty |= _failed
        
    #     logger.debug("sync")