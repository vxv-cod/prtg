__all__ = ["router"]


import time
from typing import Annotated
from celery import Task
from fastapi import APIRouter, Depends
from prtg.prtg_schema import Schema_tasks_in, Schema_tasks_out
from loguru import logger
from tasks.celery_app import celery_app


from tasks.service import Tasks_Service
from tasks.schemas import Schema_CelerySchedule, Schema_add_PeriodicTask, Schema_beat_schedule
from tasks.tasks_uow import SyncUnitOfWork

from sqlalchemy_celery_beat.models import PeriodicTaskChanged, PeriodicTask


router = APIRouter(prefix="/task", tags=["Celery task"])

task_input = Annotated[Schema_tasks_in, Depends()]
Task_depend_UOW = Annotated[SyncUnitOfWork, Depends()]
Celeri_depend_Schedule = Annotated[Schema_CelerySchedule, Depends()]
depend_NewPeriodicTask = Annotated[Schema_add_PeriodicTask, Depends()]


@router.get("/add_task_sync")
def add_task_sync(items: task_input):
    task: Task = Tasks_Service.add_task_sync
    kwargs = Schema_tasks_out.model_validate(items.model_dump()).model_dump()
    for day in items.list_days:
        task.apply_async(args=[day], kwargs={**kwargs})

    return f"Импорт с {items.sdate} - по {items.edate}"


@router.get("/add_or_update_periodic_task")
# def add_or_update_periodic_task(name: str, task: str, every: int, enabled: bool, tasks_uow: Task_depend_UOW):
def add_or_update_periodic_task(tasks_uow: Task_depend_UOW, items: depend_NewPeriodicTask):
    return Tasks_Service.add_or_update_periodic_task(tasks_uow, items)


@router.put("/stop_periodic_tasks")
def stop_periodic_tasks(id: int, tasks_uow: Task_depend_UOW):
    return Tasks_Service.stop_periodic_tasks(id, tasks_uow)


@router.delete("/delete_periodic_tasks")
def delete_periodic_tasks(id: int, tasks_uow: Task_depend_UOW):
    return Tasks_Service.delete_periodic_tasks(id, tasks_uow)


@router.get("/get_periodic_tasks")
def get_periodic_tasks(tasks_uow: Task_depend_UOW):
    return Tasks_Service.get_periodic_tasks(tasks_uow)


@router.get("/test")
def test(id: int):
    stop_task = Tasks_Service.stop_periodic_tasks(id, SyncUnitOfWork())
    logger.debug(f"{stop_task = }")
    # return stop_task
    # time.sleep(1)
    del_task = Tasks_Service.delete_periodic_tasks(id, SyncUnitOfWork())
    logger.success(f"{del_task = }")
    return del_task

from celery import Celery
from celery.beat import Service
from celery.app.control import Control, Inspect


@router.get("/edit_backend_cleanup")
def edit_backend_cleanup(tasks_uow: Task_depend_UOW, id: int = 34):
    # with tasks_uow:
    #     task = tasks_uow.session.get_one(PeriodicTask, id)
    #     task.expire_seconds = 5
    #     tasks_uow.session.commit()
    #     return task    
    # xxx_app: Celery = celery_app
    # xxx = xxx_app.__reduce_keys__()
    # logger.debug(xxx)
    # xxx = xxx_app.events
    # logger.debug(xxx)
    # xxx = xxx_app.Worker
    # xxx = xxx_app.control
    # logger.debug(xxx)
    # xxx = Service(celery_app).stop(1)
    # celery_app.close()
    # logger.debug(xxx)

    #     # celery_app.conf.beat_scheduler = CustomScheduler
    #     # CustomScheduler(celery_app).update_schedule()
    control: Control = celery_app.control
    i: Inspect = control.inspect()
    b = control.broadcast
    # control.pool_restart()
    logger.error(f"{control.heartbeat() = }")
    # control.broadcast('pool_restart', arguments={'modules': ['tasks.service'], 'reload': True})
    # control.pool_restart(modules=['tasks.service'], reload=True)
    celery_app.start


    # logger.error(f"{control.ping() = }")
    # logger.error(f"{i.stats() = }")

    # logger.error(f"{i.ping() = }")
    # logger.error(f"{i.registered() = }")
    # logger.error(f"{i.scheduled() = }")



    #     # celery@DACZC2331QT1
    #     # i = celery_app.control.inspect()
        
    #     # logger.error(f"{control.pool_restart() = }")
    #     # logger.error(f"{i.active() = }")
    #     # logger.error(f"{i.registered() = }")
    #     # logger.error(f"{i.scheduled() = }")
    #     # logger.error(f"{i.active_queues() = }")
        
    #     # '''Эта команда корректно завершит работу работника удаленно'''
    #     # celery_app.control.broadcast('shutdown')

    # def get_schedule(data: Celeri_depend_Schedule):
    #     ...


    # def update_schedule(data: Celeri_depend_Schedule):
    #     ...












# @router.get("/add_task_every_day")
# def add_schedule_task(
#     task_name: str = "task_for_every_day", 
#     name: str = "schedule_task", 
#     seconds: int = 5
#     ):
#     # task: Task = Tasks_Service.schedule_task
#     # task.apply_async(args=[name, seconds])
#     # schedule = {
#     #     task_name: {
#     #         'task': f"tasks.tasks_service.{name}", 
#     #         'schedule': seconds,
#     #         # "args": ["name!!!", 5]
#     # }}
#     # celery_app.conf.beat_schedule = {**schedule}

#     schedule = {
#         'task': f"tasks.tasks_service.{name}", 
#         'schedule': seconds,
#     }
#     celery_app.conf.beat_schedule[task_name] = schedule
#     # logger.debug(celery_app.schedule_filename)
#     # Service.scheduler_cls(celery_app).update_schedule()
#     # CustomScheduler(celery_app).tick()
#     return celery_app.conf.beat_schedule
    



# @router.post("/start_beat")
# def start_beat():
#     # celery_app.start(["worker", "--loglevel=info"])
#     Service.scheduler_cls = CustomScheduler
#     # CustomScheduler(celery_app).update_schedule()
#     Service(celery_app).start()


# @router.post("/stop_beat")
# def stop_beat():
#     celery_app.control.broadcast('shutdown')
#     Service(celery_app).sync()
#     # Service(celery_app).stop()














# @router.get("/get_tasks")
# def get_tasks():
#     return celery_app.conf.beat_schedule



# @router.post("/add_schedule")
# def add_schedule(data: Celeri_depend_Schedule):
#     data_dict = data.model_dump()
#     name_schedule = data_dict.pop("name")
#     new_schedule = celery_app.conf[name_schedule] = {**data_dict}
#     return {name_schedule: new_schedule}



    
# @router.post("/add_schedule_222")
# def add_schedule_222():
#     task: Task = Tasks_Service.schedule_task_222
#     task.apply_async()
#     # celery_app.start([
#     #     "beat", 
#     #     # "-S celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler", 
#     #     # "-l info", 
#     #     # "-s logs_celerybeat/celerybeat-schedule", 
#     #     # -s ./logs_celerybeat/celerybeat-schedule
#     #     "--loglevel=info"
#     # ])
#     # return celery_app.conf.beat_schedule
#     logger.error(schedules)
#     ...

    
    # with task_uow:
    #     query = select(CeleryScheduler)
    #     response = task_uow.session.execute(query)
    #     models: list[Base] = response.scalars().all()
    #     tasks: list[dict] = [row.to_read_model().model_dump() for row in models]

    #     for task in tasks:
    #         name_beat_schedule = task.pop("name")
    #         data_beat_schedule = Schema_beat_schedule.model_validate(task).model_dump()
    #         celery_app.conf.beat_schedule[name_beat_schedule] = data_beat_schedule
    # return celery_app.conf.beat_schedule
    

# @router.post("/update_schedule__")
# def update_schedule__():

#     # celery_app.conf.beat_scheduler = CustomScheduler
#     # CustomScheduler(celery_app).update_schedule()
#     # control = celery_app.control
#     # celery@DACZC2331QT1
#     # logger.error(control.ping())
#     # i = celery_app.control.inspect()
    
#     # logger.error(f"{control.pool_restart() = }")
#     # logger.error(f"{i.active() = }")
#     # logger.error(f"{i.registered() = }")
#     # logger.error(f"{i.scheduled() = }")
#     # logger.error(f"{i.active_queues() = }")
    
#     # '''Эта команда корректно завершит работу работника удаленно'''
#     # celery_app.control.broadcast('shutdown')

#     return "Обновлены задачи"
    


# @router.get("/add_task_every_day")
# def add_task_every_day(seconds: int):
#     task: Task = Tasks_Service.add_task_sync
#     celery_app.add_periodic_task(
#         schedule = seconds, 
#         # sig = 'tasks.tasks_service.add_task_sync', 
#         sig = task, 
#         args = [datetime.datetime.now().date() - datetime.timedelta(days=1)], 
#         kwargs = {"hours" : 1, "stime" : "08-00-00", "etime" : "18-00-00"},
#         name = 'add_every_seconds'
#     )    


# @router.get("/add_task_every_day")
# def add_task_every_day(seconds: int):
#     task: Task = Tasks_Service.setup_periodic_tasks
#     # kwargs = Schema_tasks_out.model_validate(items.model_dump()).model_dump()

#     return task.apply_async((seconds))




    # task: Task = Tasks_Service.add_task_sync
    # logger.debug(task.name)
    # schedule = {
    #     '"Задача по будням данных за вчерашние сутки"': {
    #         'task': 'tasks.tasks_service.add_task_sync',
    #         # 'schedule': crontab(hour=16, minute=31, day_of_week=1),
    #         # 'schedule': 10.0,
    #         'schedule': seconds,
    #         # 'schedule': crontab(hour = 17, minute = 7, day_of_week="2,3,4,5,6"),
    #         'args': [datetime.datetime.now().date() - datetime.timedelta(days=1)],
    #         'kwargs': {"hours" : 1, "stime" : "08-00-00", "etime" : "18-00-00"}
    #     }}
    # celery_app.add_periodic_task(
    #     schedule = seconds, 
    #     # sig = 'tasks.tasks_service.add_task_sync', 
    #     sig = task, 
    #     args = [datetime.datetime.now().date() - datetime.timedelta(days=1)], 
    #     kwargs = {"hours" : 1, "stime" : "08-00-00", "etime" : "18-00-00"},
    #     name = 'add_every_seconds'
    # )




# @router.get("/test_2")
# def test(items: Prtg_depend_historydata_input):
#     with asyncio.get_event_loop as loop:
#         for index in range(items.count_days):
#             # sync_result = sync.coroutine(__class__.add_task.delay(index, items.model_dump()))    
#             Tasks_Service.add_task.delay(index, items.model_dump())



# @router.get("/add_task_import_historydata_in_DB")
# def add_task_import_historydata_in_DB(items: Prtg_depend_historydata_input):
#     Tasks_Service().add_task_import_historydata_in_DB.delay(items.model_dump())

