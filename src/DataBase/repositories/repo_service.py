import io
from sqlalchemy import delete
from loguru import logger
from fastapi_cache.decorator import cache


from DataBase.repositories.repo_uow import UnitOfWork
from DataBase.repositories.repo_SQLAlchemy import SQLAlchemyRepository



class DB_Service:
    def __init__(self, attr_uow_name):
        self.attr_uow_name = attr_uow_name
    

    @staticmethod
    def async_with_uow(func):
        '''Декоратор для контекстного менеджера'''
        # @cache(expire=30)
        async def wrapper(self, uow, *args, **kwargs):
            async with uow:
                return await func(self, uow, *args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    

    def uow_attr(self, uow: UnitOfWork) -> SQLAlchemyRepository:
        '''Нахождение значения атирибута по имени репозитория DataBase'''
        return getattr(uow, self.attr_uow_name)


    @async_with_uow
    async def get_one(self, uow: UnitOfWork, id: int):
        '''Получение одной строки по id'''
        return await self.uow_attr(uow).get_one(id)
    

    @async_with_uow
    async def get_all(self, uow: UnitOfWork):
        '''Получение всех строк'''
        return await self.uow_attr(uow).get_all()
    

    @async_with_uow
    async def get_all_id(self, uow: UnitOfWork):
        '''Получение всех строк'''
        return await self.uow_attr(uow).get_all_id()
        

    @async_with_uow
    async def select_filter_id_in_list(self, uow: UnitOfWork, data: list[int]):
        '''Получение строк из списка id строк'''
        return await self.uow_attr(uow).select_filter_id_in_list(data)


    @async_with_uow
    async def get_all_filter(self, uow: UnitOfWork, filter_table_name: str, model_col: str):
        table_id_list: SQLAlchemyRepository = getattr(uow, filter_table_name)
        filter_list = await table_id_list.get_all_id()
        '''Получение строк из списка id строк'''
        repo = self.uow_attr(uow)
        model_col = getattr(repo.model, model_col)
        return await repo.get_all_filter(model_col, filter_list)


    @async_with_uow
    async def delete_list(self, uow: UnitOfWork, data: list[int]):
        '''Удаление строк из списка id строк'''
        res = await self.uow_attr(uow).delete_list(data)
        await uow.commit()
        return res


    @async_with_uow
    async def add_one(self, uow: UnitOfWork, data: dict):
        """Добавление одной строки из объекта"""
        res = await self.uow_attr(uow).add_one([data])
        await uow.commit()
        return res


    @async_with_uow
    async def add_list(self, uow: UnitOfWork, data: list[dict]):
        '''Добавление строк из списка с объектами'''
        res = await self.uow_attr(uow).add_list(data)
        await uow.commit()
        return res            


    @async_with_uow
    async def replace_all(self, uow: UnitOfWork, data: list[dict]):
        '''Удаляем все строки таблицы и вставляем новые'''
        db_repo = self.uow_attr(uow)
        '''Удаляем все строки в таблице'''
        await db_repo.session.execute(delete(db_repo.model))
        await uow.session.flush()
        '''Добавление новых строк'''
        res = await db_repo.add_list(data)
        await uow.commit()
        return res            


    @async_with_uow
    async def update_one(self, uow: UnitOfWork, data: dict):
        '''Обновление одной строки'''
        res = await self.uow_attr(uow).update_one(data)
        await uow.commit()
        return res


    @async_with_uow
    async def update_list(self, uow: UnitOfWork, data: list[dict]):
        '''Обновление строк из списка'''
        res = await self.uow_attr(uow).update_list(data)
        await uow.commit()
        return res
    
    

    @async_with_uow
    async def save_in_db(self, uow: UnitOfWork, data: list[dict]):
        '''Обновление или вставка строк'''
        res = await self.uow_attr(uow).save_in_db(data)
        await uow.commit()
        return res
    
    

    # @async_with_uow
    # async def upsert(self, uow: UnitOfWork, data: list[dict]):
    #     '''Обновление или вставка строк'''
    #     res = await self.uow_attr(uow).upsert(data)
    #     await uow.commit()
    #     return res
    
    async def upload_data_from_xlsx(self, uow, file, function):
        '''Полчение файла от фронта, обработка данных по function и помещение данных в ДБ'''
        data = function(io.BytesIO(file))
        
        return await self.save_in_db(uow, data)


