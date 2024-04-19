import io
import os
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger
from openpyxl import load_workbook
from rich import print
from sqlalchemy import select
from DataBase.collections.db_models_repo import SensorsRepository, UserRepository

from DataBase.dependencies.dep_uow import DataBase_depend_UOW
from DataBase.models.sensors import Sensors, TypeSensor
from DataBase.repositories.repo_servises import DB_Service
from DataBase.schemas.basemodel import Base_Model
from prtg.prtg_schema import Prtg_schema_import_in_DB_id_Int

from typing import Annotated, Any, Optional, Type

from utils.import_zgd import load_zgd
import utils.functions as my_func



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
        async def get_items_filter_by_users_zgd(uow: DataBase_depend_UOW):
            data = await self.service.get_all_filter(uow, filter_table_name = "user_zgd", model_col = "pk_name")
            return {"count": len(data), "data": data}
    

        @self.router.get("/get_items_filter_by_users_zgd_only_id", tags=self.tags)
        async def get_items_filter_by_users_zgd_only_id(uow: DataBase_depend_UOW):
            data = await get_items_filter_by_users_zgd(uow)
            data = [i["id"] for i in data["data"]]
            return {"count": len(data), "data": data}










class Api_DB_type_sensor(Api_DB_default):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)


        # @self.router.put("/save_in_db", tags=self.tags, 
        #                  response_model = Prtg_schema_import_in_DB_id_Int)
        # async def save_in_db(uow: DataBase_depend_UOW, data: list[self.db_shama_in]):
        #     return await self.service.save_in_db(uow, self.dto_in_py(data))


        @self.router.post("/default", tags=self.tags,
                         response_model = Prtg_schema_import_in_DB_id_Int)
        async def default(uow: DataBase_depend_UOW):
            return await self.service.save_in_db(uow, self.default_data)
            

class Api_DB_user_zgd(Api_DB_default):
    def __init__(self, prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid):
        super().__init__(prefix, tags, attr_uow_name, db_shama_in, db_shama_out, typeid)


        @self.router.post("/upload_file_xlsx", tags=self.tags)
        async def upload_file_xlsx(
            uow: DataBase_depend_UOW, 
            file: Annotated[bytes, File()],
            background_tasks: BackgroundTasks,
        ):
            background_tasks.add_task(self.service.upload_data_from_xlsx, uow, file, function=load_zgd)
            return "Задачи выполняются в фоне"


        @self.router.get("/download_file_xlsx", tags=self.tags)
        async def download_file_xlsx(filename: str):
            some_file_path = f'src/store/{filename}'
            headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
            return FileResponse(path=some_file_path, headers=headers)
















        # @self.router.post("/upload_file_xlsx_test", tags=self.tags)
        # async def upload_file_xlsx_test(
        #     uow: DataBase_depend_UOW, 
        #     file: Annotated[bytes, File()],
        #     background_tasks: BackgroundTasks, 
        # ):
        #     # return await self.service.save_in_db(uow, load_zgd(io.BytesIO(file)))

        #     background_tasks.add_task(self.service.save_in_db, uow, load_zgd(io.BytesIO(file)))
        #     return "Задачи выполняются в фоне"







        # @self.router.post("/upload_file_xlsx_test", tags=self.tags)
        # async def upload_file_xlsx_test(uow: DataBase_depend_UOW, file: Annotated[bytes, File()]):
            # import tempfile
            # with tempfile.NamedTemporaryFile(mode="w+b", suffix=".xlsx", delete=False) as temp_file:
            #     temp_file.write(file)            
            #     data = load_zgd(temp_file)
            # return await self.service.save_in_db(uow, data)








            # print(UploadFile.file.read())
            # buffer = io.BytesIO()
            # with UploadFile.file as temp_file:
            #     temp_file.write(buffer.getvalue())
            #     print(f"{buffer.getvalue()}")
            # xxx = load_zgd(temp_file.name)
            # print(xxx)

            # load_zgd(UploadFile.file.name)
            
            # temp_file.write(buffer.getvalue())
            # buffer = io.BytesIO()
            # file.file(mode="w+b", suffix=".xlsx", delete=False)
            # file.write(buffer.getvalue())
            # print(UploadFile.__dict__)
            # xxx = load_zgd(UploadFile.file)
            # print(xxx)
            

            return "dddddd"


            # return await self.service.save_in_db(uow, UploadFile.file.name)



            # await file.SpooledTemporaryFile
            # buffer = io.BytesIO()
            # '''Сохранение документа в буфер обмена'''
            # # file.save(buffer)
            # buffer.seek(0)

            # data = load_zgd(buffer)
            # return data
            # return await self.service.save_in_db(uow, data)
        




        # async def add_from_xlsx(uow: DataBase_depend_UOW, data: load_zgd = Depends()):
        # async def add_from_xlsx(uow: DataBase_depend_UOW, file: Annotated[UploadFile, File()]):
        # async def add_from_xlsx(uow: DataBase_depend_UOW, file: UploadFile):
        #     print(f"{file.headers = }")
        #     print(f"{file.content_type = }")
        #     print(f"{file.content_type = }")

        #     xxx = load_zgd(file)
        #     # print(f"{await file.read() = }")
        #     return {"filename": file.filename}







        
        
        # @self.router.delete("/delete_list", tags=self.tags)
        # async def delete_list(uow: DataBase_depend_UOW, data: list[int]):
        #     return await self.service.delete_list(uow, data)
        

        # @self.router.get("/get_all_id")
        # async def get_all_id(uow: DataBase_depend_UOW):
        #     return await self.service.get_all_id(uow)


        # @self.router.post("/add_one")
        # async def add_one(uow: DataBase_depend_UOW, data: self.db_shama):
        #     return await self.service.add_one(uow, data.model_dump())


        # @self.router.post("/add_list", tags=self.tags)
        # async def add_list(uow: DataBase_depend_UOW, data: list[self.db_shama]):
        #     return await self.service.add_list(uow, [row.model_dump() for row in data])


        # @self.router.put("/update_one")
        # async def update_one(uow: DataBase_depend_UOW, data: self.db_shama):
        #     return await self.service.update_one(uow, data.model_dump())


        # @self.router.put("/update_list", tags=self.tags)
        # async def update_list(uow: DataBase_depend_UOW, data: list[self.db_shama]):
        #     return await self.service.update_list(uow, self.dto_in_py(data))