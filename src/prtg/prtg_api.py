# __all__ = ['router']

import datetime
from fastapi import APIRouter, BackgroundTasks, Depends
from loguru import logger
from time import time
from DataBase.schemas.historydata import DB_schema_Log_hist_out, DataBase_schema_historydata
from DataBase.schemas.sensors import DataBase_schema_sensor

from config import Settings

from prtg.prtg_service import PRTG_Service
from prtg.prtg_schema import Prtg_schema_import_in_DB_id_Int, Prtg_schema_import_in_DB_historydata
from prtg.prtg_depends import Prtg_depend_UOW, Prtg_depend_historydata_input

from DataBase.repositories.repo_servises import DB_Service
from DataBase.dependencies.dep_uow import DataBase_depend_UOW



router = APIRouter(
    prefix="/prtg",
    tags=["Prtg:"],
)


@router.get("/import_sensors_in_DB", 
            # response_model = Prtg_schema_import_in_DB_id_Int
            )
async def import_sensors_in_DB(uow_prg: Prtg_depend_UOW, uow: DataBase_depend_UOW):
    return await PRTG_Service().import_sensors_in_DB(uow_prg, uow)


@router.get("/import_historydata_in_DB")
async def import_historydata_in_DB(
    uow_prg: Prtg_depend_UOW, 
    uow: DataBase_depend_UOW, 
    items: Prtg_depend_historydata_input, 
    background_tasks: BackgroundTasks
):
    # return await PRTG_Service().multi_import_historydata_in_DB(uow_prg, uow, items)
    background_tasks.add_task(PRTG_Service().import_historydata_in_DB, uow_prg, uow, items)
    return "Задачи выполняются в фоне"




