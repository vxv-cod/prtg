__all__ = ["UOW_Schedule"]


from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy_celery_beat.session import SessionManager
from typing import Annotated, Any
from fastapi import Depends
from tasks.tasks_schemas import Schema_get_PeriodicTask

from tasks.schedule_SQL import DBScheduler_query
from config import settings


# session_manager = SessionManager()
# session_factory = session_manager.session_factory(settings.BEAT_DBURL)

class UOW_Schedule:
    def __init__(self):
        session_manager = SessionManager()
        self.session_factory = session_manager.session_factory(settings.BEAT_DBURL)
        self.schema = None
    
    def __call__(self, schema):
        self.schema = schema
        return self

    def __enter__(self):
        self.session: Session = self.session_factory
        self.query = DBScheduler_query(session=self.session)

    def __exit__(self, *args):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


    '''----------------------------------------------------------------------------'''
    '''Вариант с колбэком менеджера контекста'''
    # def __call__(self, *args, **kwargs):
    #     self.args, self.kwargs = args, kwargs
    #     return self
    
    # def __enter__(self):
    #     self.query = DBScheduler_query(self.session, **self.kwargs)
    '''----------------------------------------------------------------------------'''