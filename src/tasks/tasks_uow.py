__all__ = ["Sync_UnitOfWork"]
__all__ = ["SyncUnitOfWork"]


from sqlalchemy.orm import Session
from sqlalchemy_celery_beat.session import SessionManager
from typing import Annotated
from fastapi import Depends

from tasks.tasks_query import DBScheduler_query
from config import settings


# session_manager = SessionManager()
# session_factory = session_manager.session_factory(settings.BEAT_DBURL)

class SyncUnitOfWork:
    def __init__(self):
        # self.session_factory = session_factory
        session_manager = SessionManager()
        self.session_factory = session_manager.session_factory(settings.BEAT_DBURL)
    
    def __enter__(self):
        self.session: Session = self.session_factory
        self.query = DBScheduler_query(self.session)

    def __exit__(self, *args):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


