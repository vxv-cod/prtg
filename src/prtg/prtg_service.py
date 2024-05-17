__all__ = ["PRTG_Service"]
import datetime
from time import time

from loguru import logger
from rich import print

from DataBase.repositories.repo_service import DB_Service
from DataBase.repositories.repo_uow import UnitOfWork
from prtg.prtg_depends import Prtg_depend_UOW, Prtg_depend_historydata_input
from prtg.prtg_uow import Prtg_UOW
from prtg.prtg_schema import Prtg_schema_historydata_input

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


    def timer_(func):
        async def parent_wrap(self, uow_prg, uow, *args):
            start_time = time()
            res = await func(self, uow_prg, uow, *args)
            logger.success(f'"{func.__name__}" : {round(time() - start_time, 8)} sec')
            return res
        return parent_wrap
    

    def async_with_uow_prg(func):
        '''Декоратор для контекстного менеджера'''
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
        # sensors = sensors[-11:]
        sensors = sensors[:50]
        # print(f"{sensors[0] = }")
        return await uow_prg.query.historydata(sensors, items)
        

    async def logging_db(self, uow: UnitOfWork, import_data):
        log_data = {
            "id": import_data["date"],
            "count_sensors": import_data["count"],
            "status": import_data["status"],
        }
        async with uow:
            current_logging = await uow.logging_download.get_all_id()
            # logger.warning(current_logging)
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
                # res = {"id": res, "status": "insert"}


            await uow.commit()
            return res
    


    async def import_sensors_in_DB(self, uow_prg: Prtg_UOW, uow: UnitOfWork):
        data = await self.prtg_get_sensors(uow_prg, uow)
        return await self.DB_Service_sensors.save_in_db(uow, data)
    


        
        
    # async def import_sensors_in_DB(self, uow_prg: Prtg_UOW, uow: UnitOfWork):
    #     data = await self.prtg_get_sensors(uow_prg, uow)
    #     print(f"{len(data) =}")
    #     async with uow:        
    #         users_id_list = await self.DB_Service_user_zgd.get_all_id(uow)
    #         data_filter = [i for i in data if i["pk_name"] in users_id_list]
    #         print(f"{len(data_filter) =}")

    #         return [len(data_filter), data_filter]

            # return await self.DB_Service_sensors.save_in_db(uow, data)
        











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
                obj_dict = {}
                
                _items = {"hours": hours, "stime": stime, "etime": etime,  "sdate": curday}
                import_data = Prtg_schema_historydata_input(**_items)

                data = await self.prtg_get_historydata(uow_prg, uow, import_data)
                obj_dict =  await self.DB_Service_historydata.save_in_db(uow, data)

                status = True
                kwargs = {"date": curday, "status": status, **obj_dict}
            except:
                kwargs = {"date": curday, "status": False, "count": 0}
            finally:
                res = await self.logging_db(uow, kwargs)
                resulst.append(res)
        print(f"{resulst = }")
        return resulst




















        # if delta.list_id_update != []:
        #     update_list = await self.update_list([row for row in data if row["id"] in delta.list_id_update])
        # if delta.list_id_insert != []:
        #     insert_list = await self.add_list([row for row in data if row["id"] in delta.list_id_insert])

        # return await self.DB_Service_logging_download.save_in_db(uow, log_data)
    
    
        # async with uow:
        #     current_logging = await uow.logging_download.get_all()
        #     logger.debug(current_logging)
        #     if current_logging != []:

        
        # async with uow:
        #     ddd = LoggingDownload(**log_data)
        #     logger.debug(ddd.id)
        #     uow.session.add(ddd)
        #     await uow.session.commit()

        # return ddd
        # async with uow:
        #     current_logging = await uow.logging_download.get_all()
        #     logger.warning(current_logging)
        #     if current_logging != []:
        #         for i in current_logging:
        #             data_dict = {"id": i["id"], **log_data}
        #             logger.debug(log_data)
        #             if i["date_of_the_data"] == items.sdate:
        #                 await uow.logging_download.update_one(data_dict)
        #             else:
        #                 await uow.logging_download.add_list(data_dict)
        #         else:
        #             data_dict = {"id": 0, **log_data}
        #             logger.debug(log_data)
                    
        #             await uow.logging_download.add_list(data_dict)

        #     await uow.commit()
        #     return data_dict





        '''Другой вариант кода'''
        # async with uow:
        #     sensors = await uow.sensors.get_all()
        #     sensors = sensors[:10]

        # async with uow_prg:
        #     historydata = await uow_prg.query.historydata(sensors, items)
        #     data  = [i.model_dump() for i in historydata]
        
        # async with uow:
        #     res = await uow.historydata.save_in_db(data)
        #     await uow.commit()
        #     return res        


