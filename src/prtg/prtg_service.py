__all__ = ["PRTG_Service"]
import datetime
from functools import wraps
from time import time
from typing import Annotated
from fastapi import Depends

from loguru import logger
from rich import print
from DataBase.models.historydata import LoggingDownload

from DataBase.repositories.repo_service import DB_Service
from DataBase.repositories.repo_uow import UnitOfWork
from prtg.prtg_uow import Prtg_UOW
from prtg.prtg_schema import Prtg_schema_historydata_input, Prtg_schema_historydata_input_OneDay


# from tasks.tasks import celery_app

# from test.test_tasks.create_celery import celery_app




# from tasks.collections_tasks import celery_app

# @celery_app.task
# def eee_task_decor():
#     # return settings.REDIS_URL
#     return "hhhhhh"


# from tasks.tasks import celery_app_2



# @celery_app_2.task
# def PRTG_Service_add_task():
#     return PRTG_Service().import_historydata_in_DB(uow_prg=Prtg_UOW, uow=UnitOfWork, items=Prtg_schema_historydata_input)


class PRTG_Service:

    def __init__(self) -> None:
        self.DB_Service_type_sensor = DB_Service("type_sensor")
        self.DB_Service_sensors = DB_Service("sensors")
        self.DB_Service_historydata = DB_Service("historydata")
        self.DB_Service_logging_download = DB_Service("logging_download")
        self.DB_Service_user_zgd = DB_Service("user_zgd")
        self.DB_Service_division = DB_Service("division")
        


    def timer_(func):
        async def parent_wrap(self, uow_prg, uow, *args):
            start_time = time()
            res = await func(self, uow_prg, uow, *args)
            logger.success(f'"{func.__name__}" : {round(time() - start_time, 8)} sec')
            return res
        return parent_wrap
    

    def async_with_uow_prg(func):
        '''Декоратор для контекстного менеджера'''
        @wraps(func)
        async def wrapper(self, uow_prg, *args, **kwargs):
            async with uow_prg:
                return await func(self, uow_prg, *args, **kwargs)
        return wrapper
    

    @async_with_uow_prg
    async def prtg_get_sensors(self, uow_prg: Prtg_UOW, uow: UnitOfWork):
        type_sensor = await self.DB_Service_type_sensor.get_all(uow)
        return await uow_prg.query.sensors(type_sensor)


    @async_with_uow_prg
    async def prtg_get_historydata(self, uow_prg: Prtg_UOW, uow: UnitOfWork, items: Prtg_schema_historydata_input):
        sensors = await self.DB_Service_sensors.get_all(uow)
        
        '''УБРАТЬ ЭТУ СТРОКУ ------------------------------------------------'''
        # sensors = sensors[:150]
        '''------------------------------------------------------------------'''
        
        return await uow_prg.query.historydata(sensors, items)
        

    async def logging_db(self, uow: UnitOfWork, import_data):
        log_data = {
            "id": import_data["date"],
            "count_sensors": import_data["count"],
            "status": import_data["status"],
        }
        async with uow:
            current_logging = await uow.logging_download.get_all_id()
            if current_logging != []:
                if log_data["id"] in current_logging:
                    res = await uow.logging_download.update_one(log_data)
                    res = {"date": res, "status": "update"}
                else:
                    res = await uow.logging_download.add_one(log_data)
                    res = {"date": res, "status": "insert"}
            else:
                res = await uow.logging_download.add_one(log_data)
                res = {"date": res, "status": "insert"}
            await uow.session.flush()
            # await uow.session.commit()
            return res


    
    async def add_zgd_divisions_in_history(self, uow: UnitOfWork, history_data):
        logger.debug("Данные получены, обрабатываются . . .")
        divisions = await uow.division.get_all()
        user_zgd = await uow.user_zgd.get_all()                                               
        res_list = []
        for hist in history_data:
            for use in user_zgd:
                if hist["pk_name"] == use["id"]:
                    for div in divisions:
                        if use["description"] == div["name"]:
                            hist["zgd_id"] = div["zgd_id"]
                            hist["division_id"] = div["id"]
            res_list.append(hist)            
        logger.debug("Данные обработаны.")
        return res_list
    


    async def import_sensors_in_DB(self, uow_prg: Prtg_UOW, uow: UnitOfWork):
        data = await self.prtg_get_sensors(uow_prg, uow)
        return await self.DB_Service_sensors.save_in_db(uow, data)
    
    
    # @timer_
    async def import_historydata_in_DB(self, uow_prg: Prtg_UOW, uow: UnitOfWork, items: Prtg_schema_historydata_input):
        '''Выбираем в интервале начальной и конечной даты (historydata) по дням и импортируем в ДБ с логами в таблицу'''

        resulst =[]
        hours = items.hours
        stime = items.stime
        etime = items.etime

        for i in range(items.count_days):
            curday = items.sdate + datetime.timedelta(days = i)
            try:
                _items = {"hours": hours, "stime": stime, "etime": etime,  "sdate": curday}
                import_data = Prtg_schema_historydata_input(**_items)

                history_data = await self.prtg_get_historydata(uow_prg, uow, import_data)
                
                async with uow:
                    history_data = await self.add_zgd_divisions_in_history(uow, history_data)
                
                result_save =  await self.DB_Service_historydata.save_in_db(uow, history_data)

                status = True
                kwargs = {"date": curday, "status": status, **result_save}
            except:
                kwargs = {"date": curday, "status": False, "count": 0}
            finally:
                res = await self.logging_db(uow, kwargs)
                resulst.append(res)
                await uow.session.commit()
        print(f"{resulst = }")
        return resulst



    async def import_historydata_task_body(self, uow_prg: Prtg_UOW, uow: UnitOfWork,
        items: Annotated[Prtg_schema_historydata_input_OneDay, Depends()]):
        
        items = Prtg_schema_historydata_input_OneDay(**items)
        sdate = items.sdate

        log_data = dict(id = sdate, status = False, count_sensors = 0)
        async with uow:
            sensors = await uow.sensors.get_all()
            # sensors = sensors[:10]
        history_data = None

        async with uow_prg:
            history_data = await uow_prg.query.historydata(sensors, items)

        async with uow:
            save_history = {"count": 0}
            logsdb = None

            if history_data:
                history_data = await self.add_zgd_divisions_in_history(uow, history_data)
                save_history = await uow.historydata.save_in_db(history_data)
                log_data.update(status = True, count_sensors = save_history["count"])
            
            logsdb = await uow.session.get(LoggingDownload, sdate)
            if not logsdb:
                res = await uow.logging_download.add_one(log_data)
                response = {"date": res, "status": "insert"}
            else:
                res = await uow.logging_download.update_one(log_data)
                response = {"date": res, "status": "update"}
            logger.success(f"response: {response}")
            await uow.commit()  
            return response  
    


    async def historydata_unit(self, uow_prg: Prtg_UOW, uow: UnitOfWork,
        items: Annotated[Prtg_schema_historydata_input, Depends()],
        sensors: int
        ):
        # 14680
        # 2024-01-02
        # logger.debug(f"{items = }") 
        items = Prtg_schema_historydata_input_OneDay(**items.model_dump())
        logger.debug(f"{items = }") 

        async with uow:
            sensors = await uow.sensors.get_one(sensors)
        logger.debug(f"{sensors = }") 

        async with uow_prg:
            history_data = await uow_prg.query.historydata([sensors], items)
        # logger.debug(f"{history_data = }") 
        
        return history_data  
    