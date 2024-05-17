__all__ = ["Tasks_Service"]

import datetime
import async_to_sync as sync
from loguru import logger
import nest_asyncio

from DataBase.repositories.repo_uow import UnitOfWork
from prtg.prtg_depends import Prtg_depend_historydata_input
from prtg.prtg_schema import Prtg_schema_historydata_input
from prtg.prtg_uow import Prtg_UOW
from prtg.prtg_service import PRTG_Service
from tasks.celery_app import celery_app
from tasks.schemas import Schema_add_PeriodicTask
from tasks.tasks_uow import SyncUnitOfWork


from sqlalchemy_celery_beat.models import PeriodicTask, IntervalSchedule, Period, PeriodicTaskChanged
from sqlalchemy_celery_beat.session import SessionManager, session_cleanup
from sqlalchemy_celery_beat.schedulers import DatabaseScheduler, ModelEntry
from config import settings



class Tasks_Service:
    
    def decor_sync(function, loop = None):
        def call(*params, **kwparams):
            async_coroutine = function(*params, **kwparams)
            nest_asyncio.apply()
            return sync.coroutine(async_coroutine, loop)
        return call
    

    @staticmethod
    @decor_sync
    async def task_body(day: datetime.date, hours: int, stime: str, etime: str):
        uow_prg = Prtg_UOW()
        uow = UnitOfWork()
        try:
            obj_dict = {}
            _items = {"hours": hours, "stime": stime, "etime": etime,  "sdate": day}
            import_data = Prtg_schema_historydata_input(**_items)
            data = await PRTG_Service().prtg_get_historydata(uow_prg, uow, import_data)
            obj_dict = await PRTG_Service().DB_Service_historydata.save_in_db(uow, data)
            data = {"date": day, "status": True, **obj_dict}
        except:
            data =  {"date": day, "status": False, "count": 0}
        finally:
            res = await PRTG_Service().logging_db(uow, data)
            logger.success(res)
            return res
            



    @celery_app.task
    def add_test_task():
        logger.success("OK")
        return "dddddddddddddddddddddd"
    

    @celery_app.task
    def add_task_sync(*args, **kwargs):
        print("ggg")
        return __class__.task_body(*args, **kwargs)



    def get_periodic_tasks(tasks_uow: SyncUnitOfWork):
        with tasks_uow:
            return tasks_uow.query.get_periodic_tasks()
        

    def add_or_update_periodic_task(tasks_uow: SyncUnitOfWork, items: Schema_add_PeriodicTask):
        with tasks_uow:
            res = tasks_uow.query.add_or_update_periodic_task(**items.model_dump())
            tasks_uow.commit()
            return res


    def stop_periodic_tasks(id: int, tasks_uow: SyncUnitOfWork):
        # with tasks_uow:
        #     res = tasks_uow.query.stop_periodic_tasks(id)
        #     tasks_uow.commit()
        #     # PeriodicTaskChanged.update_from_session(tasks_uow.session, 1)
        #     return res    

        session_manager = SessionManager()
        session = session_manager.session_factory(settings.BEAT_DBURL)
        with session_cleanup(session):
            task = session.get_one(PeriodicTask, id)
            task.enabled = False
            session.commit()
            PeriodicTaskChanged.update_from_session(session, 1)
   


    def delete_periodic_tasks(id, tasks_uow: SyncUnitOfWork):
        '''----------------------------------------------------------------------'''
        # with tasks_uow:
            # res = tasks_uow.query.delete_periodic_tasks(id)
            # tasks_uow.commit()
            # # PeriodicTaskChanged.update_from_session(tasks_uow.session, 1)
            # return res
        '''----------------------------------------------------------------------'''
        session_manager = SessionManager()
        session = session_manager.session_factory(settings.BEAT_DBURL)
        with session_cleanup(session):
            task = session.get_one(PeriodicTask, ident=id)
            session.delete(task)
            session.commit()        



            # task = session.get(PeriodicTask, ident=id)
            # session.delete(task)
            # PeriodicTaskChanged.last_change(session)
            # PeriodicTaskChanged.last_update
            # session.commit()


        # with tasks_uow:
        #     res = tasks_uow.query.stop_periodic_tasks(name)
        #     tasks_uow.commit()
        #     logger.debug(res)
        #     PeriodicTaskChanged.update_from_session(tasks_uow.session, 0)
        # with tasks_uow:
        #     PeriodicTaskChanged.update_from_session(tasks_uow.session, 1)
        # with tasks_uow:
        # with tasks_uow:
        #     PeriodicTaskChanged.update_from_session(tasks_uow.session, 0)
        #     res = tasks_uow.query.delete_periodic_tasks(name)
        #     tasks_uow.commit()
        #     logger.debug(res)
        #     PeriodicTaskChanged.update_from_session(tasks_uow.session, 1)

        #     return res

        # __class__.stop_periodic_tasks(id, tasks_uow)

        # session_manager = SessionManager()
        # session = session_manager.session_factory(settings.BEAT_DBURL)


        # PeriodicTaskChanged.last_change(session)
        # PeriodicTaskChanged.update_from_session(tasks_uow.session, 0)
        # session.commit()

        # session = session_manager.session_factory(settings.BEAT_DBURL)
        # with session_cleanup(session):

        # with tasks_uow:
        #     PeriodicTaskChanged.update_from_session(tasks_uow.session, 1)

        # with tasks_uow:
        # task = session.get(PeriodicTask, ident=id)
        # session.delete(task)
        # # fff = PeriodicTaskChanged.last_change(tasks_uow.session)
        # # logger.debug(fff)
        # # PeriodicTaskChanged.last_update = fff
        # session.commit()


            

        # task = session.get(PeriodicTask, ident=id)
        # session.delete(task)
        # PeriodicTaskChanged.last_change(session)
        # PeriodicTaskChanged.last_update
        # session.commit()
        # PeriodicTaskChanged.update_from_session(session, 1)



        # def eee():
        #     with session_cleanup(session):
        #         task = session.get(PeriodicTask, ident=id)
        #         task.enabled = 0
        #         session.add(task)
        #         session.commit()
        #         PeriodicTaskChanged.update_from_session(session, 1)
        #     return task
        
        # with session_cleanup(session):
            # task = eee()
            # session.delete(task)
            # session.commit()
            

            # PeriodicTaskChanged.update_from_session(session, 0)
        # with session_cleanup(session):
        #     task = session.get(PeriodicTask, ident=id)
        #     session.delete(task)
        #     PeriodicTaskChanged.last_change(session)
        #     session.commit()

            
        # from sqlalchemy.orm import Session

        # # with session_cleanup(session):
        # id = int(name)
        # model = session.get(PeriodicTask, ident=id)
        # xxxEntry = ModelEntry(model=model, Session=Session, app=celery_app)
        # print(xxxEntry._disable(model))
        # print(xxxEntry.update_from_dict())

        # xxxEntry.__next__()
        # xxxEntry.save(fields=tuple("schedule_id"))

        # from celery.beat import ScheduleEntry
        
        # xxx = ScheduleEntry(name="test", task="tasks.service.add_test_task", last_run_at=None,
        #          total_run_count=None, schedule=None, args=(), kwargs=None,
        #          options=None, relative=False, app=None)
        
        # xxx.schedule=33












    # @decor_sync
    # async def schedule_task_body():
    #     uow = UnitOfWork()
    #     return await DB_Service("celery_scheduler").get_all(uow)
        
    #     # logger.debug(obj_dict)
    



    # @celery_app.task
    # def schedule_task_222():
    #     celery_app.conf.beat_scheduler = CustomScheduler
    #     celery_app.start([
    #         "beat", 
    #         # "-S celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler", 
    #         # "-l info", 
    #         # "-s logs_celerybeat/celerybeat-schedule", 
    #         # -s ./logs_celerybeat/celerybeat-schedule
    #         "--loglevel=info"
    #     ])
    #     return "celery-beat запущен"


    # @celery_app.task
    # def schedule_task(*args, **kwargs):
    #     return {"args": args, "kwargs": kwargs}





        # logger.debug(name, seconds)
        # data = __class__.schedule_task_body()
        # data = data[0]
        # logger.debug(data)

        # logger.debug(data)
        # schedule = {
        #     data["name"]: {
        #         data["task"]: f'tasks.tasks_service.{data["name"]}', 
        #         'schedule': data["schedule"],
        #         # "args": ["name!!!", 5]
        # }}
        # celery_app.conf.beat_schedule = {
        #     data["name"]: {
        #         data["task"]: f'tasks.tasks_service.{data["name"]}', 
        #         'schedule': data["schedule"],
        #         # "args": ["name!!!", 5]
        # }}
        # return "Ffffffffffffff"

        # schedule = {name: {'task': "name: " + name, 'schedule': seconds}}
        # celery_app.conf.beat_schedule = {**schedule}
        # return __class__.task_body(*args, **kwargs)


    # @celery_app.on_after_configure.connect
    # def setup_periodic_tasks(seconds):
    #     # schedule = {
    #     #     '"Задача по будням данных за вчерашние сутки"': {
    #     #         'task': 'tasks.tasks_service.add_task_sync',
    #     #         # 'schedule': crontab(hour=16, minute=31, day_of_week=1),
    #     #         # 'schedule': 10.0,
    #     #         'schedule': seconds,
    #     #         # 'schedule': crontab(hour = 17, minute = 7, day_of_week="2,3,4,5,6"),
    #     #         'args': [datetime.datetime.now().date() - datetime.timedelta(days=1)],
    #     #         'kwargs': {"hours" : 1, "stime" : "08-00-00", "etime" : "18-00-00"}
    #     #     }}
    #     celery_app.add_periodic_task(
    #         schedule = seconds, 
    #         # sig = 'tasks.tasks_service.add_task_sync', 
    #         sig = __class__.add_task_sync, 
    #         args = [datetime.datetime.now().date() - datetime.timedelta(days=1)], 
    #         kwargs = {"hours" : 1, "stime" : "08-00-00", "etime" : "18-00-00"},
    #         name = 'add_every_seconds'
    #     )        




    # @celery_app.task
    # def add_task_import_historydata_in_DB(items: dict):
    #     sync_result: list[dict[str, datetime.date]] = sync.coroutine(
    #         PRTG_Service().import_historydata_in_DB(
    #             uow_prg = Prtg_UOW(), 
    #             uow = UnitOfWork(), 
    #             items = Prtg_schema_historydata_input.model_validate(items)
    #     ))
    #     for row in sync_result:
    #         row["id"] = row["id"].isoformat()

    #     return sync_result
    

    # @celery_app.task
    # def add_task_for_async_loop(*args, **kwargs):
    #     '''------------------------------------------------------------'''
    #     '''Работают при pool=solo'''
    #     # nest_asyncio.apply()
    #     # return celery_loop.run_until_complete(__class__.task_body(*args, **kwargs))
    #     # return asyncio.run(__class__.task_body(*args, **kwargs))
    #     '''------------------------------------------------------------'''


