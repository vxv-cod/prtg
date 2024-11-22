__all__ = ["TasksRepository"]

import asyncio
import datetime
from functools import wraps
import nest_asyncio
from loguru import logger
from DataBase.repositories.repo_service import DB_Service

from DataBase.repositories.repo_uow import UnitOfWork
from prtg.prtg_service import PRTG_Service
from prtg.prtg_uow import Prtg_UOW
from tasks.celery_app import celery_app



class TasksRepository:

    def get_all_task_name() -> list[tuple[str, str]]:
        '''Собираем все задачи и делаем список из кортежей (полное имя, имя)'''
        tasks: dict = celery_app._tasks
        tasks_keys: list[str] = list(tasks.keys())
        result = []
        for val in tasks_keys:
            key = val.split(".")[-1]
            result.append((key, val))
        # logger.debug(result)
        return result
    

    def decor_asyncio_run(optional = lambda x: x):
        def wrapper_up(async_func):
            @wraps(async_func)
            def wrapper(*args, **kwargs):
                nest_asyncio.apply()
                res = asyncio.run(async_func(*args, **kwargs))
                respo = optional(res)
                logger.success(f"{async_func.__name__}: {respo}")
                return respo
            return wrapper
        return wrapper_up


    @staticmethod
    @decor_asyncio_run
    async def getlogs(attr_uow_name, uow: UnitOfWork = UnitOfWork()):
        return await DB_Service(attr_uow_name).get_all_id(uow)    
        

    @staticmethod
    @celery_app.task
    @decor_asyncio_run()
    def manual_import_historydata_in_DB(*args, **kwargs):
        logger.debug(f"{args = }")
        # logger.debug(f"{kwargs = }")
        # items = dict(sdate=args[0], task_kwargs=kwargs)
        items = dict(sdate=args[0], **kwargs)
        kwargs = dict(items=items, uow_prg=Prtg_UOW(), uow=UnitOfWork())
        return PRTG_Service().import_historydata_task_body(**kwargs)
    

    @staticmethod
    @celery_app.task
    @decor_asyncio_run(lambda x: x["count"])
    def import_sensors_in_DB():
        return PRTG_Service().import_sensors_in_DB(Prtg_UOW(), UnitOfWork())
    

    @staticmethod
    @celery_app.task
    @decor_asyncio_run()
    def auto_import_histor(**kwargs):
        day = datetime.datetime.now().date() - datetime.timedelta(days=1)
        # items = dict(sdate=day, task_kwargs=kwargs)
        items = dict(sdate=day, **kwargs)
        kwargs = dict(items=items, uow_prg=Prtg_UOW(), uow=UnitOfWork())
        return PRTG_Service().import_historydata_task_body(**kwargs)





    

