import io
import os
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger
from openpyxl import load_workbook
from rich import print
from sqlalchemy import select
from DataBase.collections.db_models_repo import SensorsRepository, UserRepository
from fastapi_cache.decorator import cache


from DataBase.dependencies.dep_uow import DataBase_depend_UOW
from DataBase.models.sensors import Sensors, TypeSensor
from DataBase.repositories.repo_service import DB_Service
from DataBase.schemas.basemodel import Base_Model
from prtg.prtg_schema import Prtg_schema_import_in_DB_id_Int

from typing import Annotated, Any, Optional, Type

from utils.import_zgd import set_user_zgd, save_file, set_division, set_zgd



class Api_Base:
    default_data = None
    
    def dto_in_py(self, data: list[Base_Model] | Base_Model):
        if isinstance(data, list):
            return [i.model_dump() for i in data]
        if isinstance(data, Base_Model):
            return data.model_dump()


    def __init__(self, prefix, tags, attr_uow_name, db_shama_in: Base_Model, db_shama_out, typeid):
        self.tags = tags
        self.db_shama_in = db_shama_in
        self.db_shama_out = db_shama_out
        self.router = APIRouter(prefix = prefix)
        self.service = DB_Service(attr_uow_name)
        # self.attr_uow_name = attr_uow_name
        self.typeid = typeid





class Api_DB_default(Api_Base):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)

        @self.router.get("/get_all", tags=self.tags)
        async def get_all(uow: DataBase_depend_UOW):
            #  -> list[self.db_shama_out]
            # return await self.service.get_all(uow)
            data = await self.service.get_all(uow)
            return {"count": len(data), "data": data}


        @self.router.post("/get_items_form_id_in_list", tags=self.tags)
        async def filter_list_from_id(uow: DataBase_depend_UOW, items: list[self.typeid]) -> list[self.db_shama_out]:
            return await self.service.select_filter_id_in_list(uow, items)


        @self.router.put("/save_in_db", tags=self.tags, 
                         response_model = Prtg_schema_import_in_DB_id_Int)
        async def save_in_db(uow: DataBase_depend_UOW, data: list[self.db_shama_in]):
            return await self.service.save_in_db(uow, self.dto_in_py(data))


class Api_DB_logging(Api_DB_default):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)


class Api_DB_sensors(Api_DB_default):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)



# class Api_DB_historydata(Api_DB_default):
class Api_DB_historydata(Api_Base):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)
    

        @self.router.get("/get_items_filter_by_users_zgd", tags=self.tags)
        # @cache(expire=30)
        async def get_items_filter_by_users_zgd(uow: DataBase_depend_UOW):
            data = await self.service.get_all_filter(uow, filter_table_name = "user_zgd", model_col = "pk_name")
            return {"count": len(data), "data": data}
    

        @self.router.get("/get_items_filter_by_users_zgd_only_id", tags=self.tags)
        # @cache(expire=30)
        async def get_items_filter_by_users_zgd_only_id(uow: DataBase_depend_UOW):
            data = await get_items_filter_by_users_zgd(uow)
            data = [i["id"] for i in data["data"]]
            return {"count": len(data), "data": data}
        

        @self.router.get("/set_division_id_in_history", tags=self.tags)
        async def set_division_id_in_history(uow: DataBase_depend_UOW):
            return await self.service.set_division_id_in_history(uow)

        




class Api_DB_type_sensor(Api_DB_default):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)


        @self.router.get("/default_type_sensor", tags=["default"], response_model = Prtg_schema_import_in_DB_id_Int)
        async def default_type_sensor(uow: DataBase_depend_UOW):
            return await self.service.save_in_db(uow, self.default_data)
            

class Api_DB_user_zgd(Api_DB_default):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)


        @self.router.get("/default_from_xlxs", tags=["default"])
        async def default_from_xlxs(uow: DataBase_depend_UOW):
            return await self.service.default_from_xlxs(uow, set_user_zgd)
        


        # @self.router.post("/upload_file_xlsx", tags=["default"])
        # async def upload_file_xlsx(
        #     uow: DataBase_depend_UOW, 
        #     file: Annotated[bytes, File()],
        #     background_tasks: BackgroundTasks,
        # ):
        #     # background_tasks.add_task(self.service.upload_data_from_xlsx, uow, file, function=set_user_zgd)
        #     # return "Задачи выполняются в фоне"
        #     return await self.service.upload_data_from_xlsx(uow, file, set_user_zgd)







        @self.router.get("/download_file_xlsx", tags=self.tags)
        async def download_file_xlsx(filename: str):
            some_file_path = f'src/store/{filename}'
            headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
            return FileResponse(path=some_file_path, headers=headers)
                        

class Api_DB_files():
    def __init__(self, prefix, tags):
        self.tags = tags
        self.router = APIRouter(prefix = prefix)

        @self.router.post("/upload_file", tags=self.tags)
        async def upload_file(file: UploadFile, ):
            save_file(file)
            return f"{file.filename} - загружен в хранилице store"
        
        # ZGD_111.xlsx
        @self.router.get("/download_file", tags=self.tags)
        async def download_file(filename: str):
            some_file_path = f'src/store/{filename}'
            headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
            return FileResponse(path=some_file_path, headers=headers)








class Api_DB_zgd(Api_DB_default):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)

        @self.router.get("/default_from_xlxs", tags=["default"])
        async def default_from_xlxs(uow: DataBase_depend_UOW):
            return await self.service.default_from_xlxs(uow, set_zgd)


class Api_DB_division(Api_DB_default):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)

        @self.router.get("/default_from_xlxs", tags=["default"])
        async def default_from_xlxs(uow: DataBase_depend_UOW):
            return await self.service.default_from_xlxs(uow, set_division)



'''
# background_tasks: BackgroundTasks

В методе с File мы получаем на выходе только байт-строку.
# file: Annotated[bytes, File()], # метод нужен для получения байт файла

Метод UploadFile несколько более интересный в плане параметров, он имеет их целый набор.
Хочешь взять имя отправленного файла? 
file.filename
Нужен сам файл, а не его байты? 
file.file
Нужны байты?
file.file.read()
'''

        