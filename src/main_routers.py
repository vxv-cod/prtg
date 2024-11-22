from prtg.prtg_api import router as router_prtg
from tasks.celery_api import router_manual as task_router_manual
from tasks.celery_api import router_periodic as task_router__periodic
from DataBase.collections.db_api import (
    api_files,
    api_user_zgd,
    api_zgd,
    api_obj_sensors, 
    api_obj_historydata, 
    api_type_sensor, 
    api_logging_download,
    api_division,
)


all_routers = [
    api_files.router,
    api_type_sensor.router,
    api_user_zgd.router,
    api_zgd.router,
    api_division.router,
    api_obj_sensors.router,
    api_obj_historydata.router,
    api_logging_download.router,
    router_prtg,

    task_router_manual,
    task_router__periodic,

]

