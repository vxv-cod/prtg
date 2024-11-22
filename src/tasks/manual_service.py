__all__ = ["TasksRepository"]

from loguru import logger
from celery import Task

from tasks.tasks_schemas import Schema_task_kwargs, Schema_tasks_in
from tasks.tasks_repo import TasksRepository



class Manual_Service:

    @staticmethod
    def import_sensors_in_DB():
        task: Task = TasksRepository.import_sensors_in_DB
        task.apply_async()


    @staticmethod
    def manual_add_or_update_task(items: Schema_tasks_in):
        '''Запросы данных из PRTG всех дней'''
        task: Task = TasksRepository.manual_import_historydata_in_DB
        kwargs = Schema_task_kwargs.model_validate(items.model_dump()).model_dump()
        logger.debug(f"{items.list_days = }")
        for day in items.list_days:
            logger.debug(f"{day = }")
            task.apply_async(args=[day], kwargs={**kwargs})
            # return res.result
        return "OK"


    @staticmethod
    def manual_add_nonexistent_days(items: Schema_tasks_in):
        '''Запросы данных из PRTG не включая уже существующие дни из логов'''
        task: Task = TasksRepository.manual_import_historydata_in_DB
        kwargs = Schema_task_kwargs.model_validate(items.model_dump()).model_dump()
        
        logs = TasksRepository.getlogs("logging_download")
        for day in items.list_days:
            if day not in logs:
                task.apply_async(args=[day], kwargs={**kwargs})
            else:
                logger.debug(f"{day} уже есть")




        # ignore_result=True
        # result = task.apply_async()
        # result = task.apply_async()
        # logger.debug(result)
        # res = result.get()
        # logger.debug(res)
        # return res