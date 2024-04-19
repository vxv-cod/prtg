from prtg.prtg_api import router as router_prtg
from DataBase.collections.db_api import (
    api_user_zgd,
    api_obj_sensors, 
    api_obj_historydata, 
    api_type_sensor, 
    api_logging_download,
)


all_routers = [
    router_prtg,
    api_type_sensor.router,
    api_user_zgd.router,
    api_obj_sensors.router,
    api_obj_historydata.router,
    api_logging_download.router,

]

