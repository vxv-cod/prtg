__all__ = ["Schedule_Service"]

from sqlalchemy_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, PeriodicTaskChanged

from tasks.tasks_schemas import Schema_add_PeriodicTask_Crontab
from tasks.schedule_uow import UOW_Schedule



class Schedule_Service:
    
    @staticmethod
    def str_in_list(string: str):
        return [int(i.strip()) for i in string.split(",")]

    @staticmethod
    def get_periodic_tasks_all(tasks_uow: UOW_Schedule):
        with tasks_uow:
            return tasks_uow.query.get_periodic_tasks_all()
        
    @staticmethod
    def add_or_update_interval_task(tasks_uow: UOW_Schedule, items: Schema_add_PeriodicTask_Crontab):
        with tasks_uow:
            res = tasks_uow.query.add_or_update_periodic_task(items, task_model=IntervalSchedule)
            PeriodicTaskChanged.update_from_session(tasks_uow.session, False)
            tasks_uow.commit()
            return res

    @staticmethod
    def add_or_update_crontab_task(tasks_uow: UOW_Schedule, items: Schema_add_PeriodicTask_Crontab):
        with tasks_uow:
            res = tasks_uow.query.add_or_update_periodic_task(items)
            PeriodicTaskChanged.update_from_session(tasks_uow.session, False)
            tasks_uow.commit()
            return res

    @staticmethod
    def start_or_stop_list_periodic_tasks(tasks_uow: UOW_Schedule, id_list: str, enabled: bool):
        with tasks_uow:
            id_list = __class__.str_in_list(id_list)
            res = tasks_uow.query.start_or_stop_list_periodic_tasks(enabled, id_list)
            PeriodicTaskChanged.update_from_session(tasks_uow.session, False)
            tasks_uow.commit()
            return res

    @staticmethod
    def delete_rows(id_list, tasks_uow: UOW_Schedule, 
        model: PeriodicTask | IntervalSchedule | CrontabSchedule
    ):
        with tasks_uow:
            id_list = __class__.str_in_list(id_list)
            res = tasks_uow.query.delete_rows(id_list, model)
            PeriodicTaskChanged.update_from_session(tasks_uow.session, False)
            tasks_uow.commit()
            return res



    # @celery_app.task
    # def add_task_for_async_loop(*args, **kwargs):
    #     '''------------------------------------------------------------'''
    #     '''Работают при pool=solo'''
    #     # nest_asyncio.apply()
    #     # return celery_loop.run_until_complete(__class__.task_body(*args, **kwargs))
    #     # return asyncio.run(__class__.task_body(*args, **kwargs))
    #     '''------------------------------------------------------------'''

    # '''----------------------------------------------------------------------'''
    # session_manager = SessionManager()
    # session = session_manager.session_factory(settings.BEAT_DBURL)
    # with session_cleanup(session):
    #     task = session.get_one(PeriodicTask, ident=id)
    #     session.delete(task)
        # session.commit()
    # '''----------------------------------------------------------------------'''
