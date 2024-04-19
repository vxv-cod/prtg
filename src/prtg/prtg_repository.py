import asyncio
import datetime
from time import time
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from rich import print

from httpx import AsyncClient, Limits, Timeout
from httpx import Response as httpx_Response
from DataBase.schemas.sensors import DataBase_schema_sensor

# from config.settings import   DEBUG, PASSHASH, PRTG_SERVER, USER
from prtg.prtg_schema import Prtg_schema_historydata_calculations, Prtg_schema_historydata_headers, Prtg_schema_historydata_input, Prtg_schema_Sensor
from loguru import logger

from config import settings


def timer_(my_func):
    '''Время выполнения'''
    # @logger.catch
    async def wrapper(*args, **kwargs):
        if settings.DEBUG == "True":
            start_time = time()
            res =  await my_func(*args, **kwargs)
            logger.success(f'"{my_func.__name__}" : {round(time() - start_time, 8)} sec')
            return res
        else: 
            return await my_func(*args)
    
    return wrapper


class PrtgRepository:

    def __init__(self, client: AsyncClient):
        self.client = client
        # self.client.timeout = Timeout(600)
        # self.client.verify = False
        # self.client.trust_env = False

    def timer_(my_func):
        '''Время выполнения'''
        # @logger.catch
        async def wrapper(*args, **kwargs):
            if settings.DEBUG == "True":
                start_time = time()
                res =  await my_func(*args, **kwargs)
                logger.success(f'"{my_func.__name__}" : {round(time() - start_time, 8)} sec')
                return res
            else: 
                return await my_func(*args)
        
        return wrapper


    # @timer_
    async def sensors(self, type_sensor):
        url = f"{settings.PRTG_SERVER}/api/table.json"
        params = {
            "content" : "sensors",
            "output" : "json",
            "columns" : "objid,device,sensor",
            "count" : "99999",
            "username" : settings.USER, "passhash" : settings.PASSHASH
            }
        response = await self.client.get(url=url, params=params)

        if response.status_code == 200:
            sensors = response.json()["sensors"]
            # logger.warning(f"Всего сенсоров = {len(sensors)}")
            filter_obj = []
            for sens in sensors:
                for item in type_sensor:
                    
                    device_rstrip = sens["device"].lstrip("TNNC-")
                    sens["pk_name"] = device_rstrip.split('.rosneft.ru')[0]
                    if item["value"] in sens["sensor"]:
                        # sens["type"] = item["type"]
                        sens["type_id"] = item["id"]
                        filter_obj.append(sens)

            # logger.debug(f"Фильтр сенсоров = {len(filter_obj)}")
            sensors_dto = [Prtg_schema_Sensor.model_validate(i) for i in filter_obj]
            sensors_py = [i.model_dump() for i in sensors_dto]
            return sensors_py
        else:
            return response
    



    # @timer_
    async def historydata(self, sensors, items: Prtg_schema_historydata_input):
        # logger.error(items.sdate)

        tasks = []
        for sensor in sensors:
            url = f"{settings.PRTG_SERVER}/api/historicdata.json"
            sensor = DataBase_schema_sensor(**sensor)
            params = {
                "id"         : f"{sensor.id}",
                "avg"        : f"{round(items.hours * 3600)}",
                "sdate"      : f"{items.sdate}-00-00-00",
                "edate"      : f"{items.sdate}-23-59-59",
                "usecaption" : "1",
                "username"   : settings.USER, 
                "passhash"   : settings.PASSHASH,
            }
            headers = {
                "sensor_id": str(sensor.id),
                "type_id": str(sensor.type_id),
                "pk_name": str(sensor.pk_name),
                "stime": items.stime,
                "etime": items.etime,
                }
                    
            task = self.client.get(url=url, params=params, headers=headers)
            tasks.append(asyncio.create_task(task))

        responses_gather_list = await asyncio.gather(*tasks)
    
        content = []
        for response in responses_gather_list:
            response: httpx_Response
            request_headers = Prtg_schema_historydata_headers(**response.request.headers).model_dump()
            if response.status_code == 200:
                request_headers['histdata'] = response.json()["histdata"]
                content.append(request_headers)
            else:
                raise HTTPException(status_code=response.status_code, detail={"response" : response, "id" : request_headers["sensor_id"]})

        content: list[Prtg_schema_historydata_calculations] = [Prtg_schema_historydata_calculations.model_validate(i) for i in content]
        content = [i for i in content if i.avg_value != 0]
        content  = [i.model_dump() for i in content]
        return content
