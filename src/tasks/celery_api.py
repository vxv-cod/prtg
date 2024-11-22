__all__ = ["router"]


from typing import Annotated
from fastapi import APIRouter, Depends
from tasks.tasks_schemas import Schema_tasks_in

from tasks.tasks_schemas import Schema_add_PeriodicTask_Crontab, Schema_add_PeriodicTask_Interval
from tasks.manual_service import Manual_Service
from tasks.schedule_service import Schedule_Service
from tasks.schedule_uow import UOW_Schedule

from sqlalchemy_celery_beat.models import PeriodicTask, CrontabSchedule
from sqlalchemy_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

router_manual = APIRouter(prefix="/task", tags=["Tasks: manual"])
router = router_manual

task_input = Annotated[Schema_tasks_in, Depends()]
Task_depend_UOW = Annotated[UOW_Schedule, Depends()]
depend_interval_task = Annotated[Schema_add_PeriodicTask_Interval, Depends()]
depend_crontab_task = Annotated[Schema_add_PeriodicTask_Crontab, Depends()]


'''Вручную указать начальную и конечную дату'''

@router.get("/manual_import_historydata_add_nonexistent_days")
def manual_import_historydata_add_nonexistent_days(items: task_input):
    return Manual_Service.manual_add_nonexistent_days(items)


@router.get("/manual_import_historydata_add_or_update_task")
def manual_import_historydata_add_or_update_task(items: task_input):
    return Manual_Service.manual_add_or_update_task(items)



@router.get("/import_sensors_in_DB")
def import_sensors_in_DB():
    return Manual_Service.import_sensors_in_DB()




'''Настройка планировщика'''

router_periodic = APIRouter(prefix="/task", tags=["Tasks: schedule"])
router = router_periodic
@router.get("/get_periodic_tasks_all")
def get_periodic_tasks_all(tasks_uow: Task_depend_UOW):
    return Schedule_Service.get_periodic_tasks_all(tasks_uow)


@router.get("/add_or_update_interval_task")
def add_or_update_interval_task(tasks_uow: Task_depend_UOW, items: depend_interval_task):
    return Schedule_Service.add_or_update_interval_task(tasks_uow, items)


@router.get("/add_or_update_crontab_task")
def add_or_update_crontab_task(tasks_uow: Task_depend_UOW, items: depend_crontab_task):
    return Schedule_Service.add_or_update_crontab_task(tasks_uow, items)


@router.get("/start_or_stop_list_periodic_tasks")
def start_or_stop_list_periodic_tasks(tasks_uow: Task_depend_UOW, id_list: str, enabled: bool = False):
    return Schedule_Service.start_or_stop_list_periodic_tasks(tasks_uow, id_list, enabled)


@router.delete("/delete_periodic_tasks")
def delete_periodic_tasks(id_list: str, tasks_uow: Task_depend_UOW):
    return Schedule_Service.delete_rows(id_list, tasks_uow, model=PeriodicTask)


@router.delete("/delete_interval_schedule")
def delete_interval_schedule(id_list: str, tasks_uow: Task_depend_UOW):
    return Schedule_Service.delete_rows(id_list, tasks_uow, model=IntervalSchedule)


@router.delete("/delete_crontab_schedule")
def delete_crontab_schedule(id_list: str, tasks_uow: Task_depend_UOW):
    return Schedule_Service.delete_rows(id_list, tasks_uow, model=CrontabSchedule)






# @router.get("/test_schedule")
# def test_schedule(id_list: str, tasks_uow: Task_depend_UOW):
#     return Schedule_Service.test_schedule(id_list, tasks_uow)
