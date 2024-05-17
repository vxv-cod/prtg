from typing import Any
from loguru import logger
from sqlalchemy import Insert, Select, delete, insert, select, update, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.db import Base

class Delta_id:
    def __init__(self, A, B):
        self.A = set(A)
        self.B = set(B)
        self.list_id_insert = list(self.A ^ self.B)
        self.list_id_update = list(self.A & self.B)
        self.count = len(list(self.A | self.B))


class SQLAlchemyRepository:
    model: Base

    def __init__(self, session: AsyncSession):
        self.session = session


    def dto_in_py(self, models: list[Base] | Base):
        if isinstance(models, list):
            return [row.to_read_model().model_dump() for row in models]
        if isinstance(models, self.model):
            return models.to_read_model().model_dump()


    async def add_one(self, data: dict):
        query = insert(self.model).returning(self.model.id)
        result = await self.session.execute(query, data)
        
        return result.scalar_one()


    async def add_list(self, data: list[dict]):
        query = insert(self.model).returning(self.model.id)
        result = await self.session.execute(query, data)
        
        return result.scalars().all()

    
    async def get_one(self, id: int):
        query = select(self.model).filter_by(id = id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model != None: 
            return self.dto_in_py(model)
        else:
            return model
    

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return self.dto_in_py(result.scalars().all())
    

    async def get_all_id(self):
        query = select(self.model.id)
        result = await self.session.execute(query)
        result = result.scalars().all()
        return result


    async def get_all_filter(self, model_col, filter_list: list[int]):
        query: Select = select(self.model)
        query.filter(model_col.in_(filter_list))
        result = await self.session.execute(query)
        return self.dto_in_py(result.scalars().all())

        
    async def select_filter_id_in_list(self, data: list[int]):
        query = select(self.model).filter(self.model.id.in_(data))
        result = await self.session.execute(query)

        return self.dto_in_py(result.scalars().all())
    

    async def delete_list(self, data: list[int]):
        query = delete(self.model).filter(self.model.id.in_(data)).returning(self.model.id)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def update_one(self, data: dict):
        # query = update(self.model).values(**data).filter_by(id = data["id"]).returning(self.model.id)
        # result = await self.session.execute(query)
        query = update(self.model).filter_by(id = data["id"]).returning(self.model.id)
        result = await self.session.execute(query, data)

        return result.scalar_one()

        
    async def update_list(self, data: list[dict]):
        return await self.session.execute(update(self.model), data)
    

    async def save_in_db(self, data: list[dict]):
        logger.debug("save_in_db")
        current_ids = await self.get_all_id()
        data_ids = [i["id"] for i in data]
        insert_list = []
        update_list = []

        for i in data_ids:
            if i in current_ids:
                update_list.append(i)
            else:
                insert_list.append(i)

        if update_list != []:
            await self.update_list([row for row in data if row["id"] in update_list])
        if insert_list != []:
            await self.add_list([row for row in data if row["id"] in insert_list])
        return {"count": len(data), "insert_list": insert_list, "update_list": update_list}
    



    '''
    async def upsert(self, data: list[dict]):
        from sqlalchemy.dialects.postgresql import insert

        stmt = insert(self.model).values(data)
        query = (stmt.on_conflict_do_update(index_elements=['id'], set_=stmt.excluded).returning(self.model.id))
        result = await self.session.execute(query)
        res = result.scalars().all()

        return {"count_data": len(data), "count_res": len(res)}
    '''




        # from DataBase.db import engine
        # if engine.dialect.name == "postgresql":
        #     print("fffffffffffffff")


        # query = insert(self.model).on_conflict_do_update(index_elements = ['id'], set_ = data, where=(self.model.id == ["id"] ))
        # from sqlalchemy.dialects.postgresql import insert
        # query = insert(self.model).on_conflict_do_nothing(index_elements = ['id'])
        # query = select(self.model.id)
        # current = await self.session.execute(query)
        # current = current.scalars().all()
        # logger.debug(current)
        
        # query = update(self.model).filter(self.model.id.in_(current))
    
    
    
    
    
        # from sqlalchemy.dialects.postgresql import insert
    
        # query = insert(self.model).values(data).on_conflict_do_nothing(index_elements=["id"]).returning(self.model.id)
        # result = await self.session.execute(query)
        # response = result.scalars().all()
        # return response
    

        # def delta_id(A, B):
        #     delta_id_insert = list(A ^ B)
        #     delta_id_update = list(A & B)
        #     return delta_id_update, delta_id_insert

        

        # logger.warning(f"{delta.list_id_update = }")


        # result = await self.session.execute(insert(self.model), delta)
        # response = result.scalars().all()
        # return response

        
        
        
        
        
        # return "result.scalars().all()"
        # logger.debug(data)

        # for i in data:
        #     print(i)            
        #     query = insert(self.model).on_conflict_do_update(index_elements = ['id'], set_ = i)
        #     await self.session.execute(query)
        #     await self.session.flush()

        # print(sqlalchemy.dialects.registry)
        # query = insert(self.model).on_conflict_do_nothing(
        #     constraint="id",
        #     index_elements=["id"],
        # )

        # xxx = [ 10009, 10012, 10016, 10022, 10033, 10035, 10037, 10038 ]
        # xxx = [10005, 10006, 10009, 10012, 10016, 10022, 10033, 10035, 10037, 10038 ]
        
        # query = Select(self.model).filter(self.model.id.not_in(xxx))
        # result = await self.session.execute(query)
        # logger.debug(query)
        
        # query = Insert(self.model).filter_by(id.not_in(xxx))
        # # .filter(self.model.id.not_in(xxx)).returning(self.model.id)
        # result = await self.session.execute(query)
        # logger.debug(query)



        # logger.debug(result.scalars().all())

        # result = await self.session.execute(query, data)
        # logger.debug(result.unique().scalars().all())
        # query = update(self.model).filter(self.model.id == id).returning(self.model.id)
            
        # result = await self.session.execute(query, data)
        
        # return result.scalars().all()
    






    
        # return DataBase_schema_sensor.model_validate(res.scalar_one())
    
    # async def find_one(self, **filter_by):
    #     query = select(self.model).filter_by(**filter_by)
    #     logger.debug(query)
    #     res = await self.session.execute(query)
    #     res = res.scalar_one().to_read_model()
    #     return res

    '''Вариант 2'''
    # async def add_all_sensors(self, items: list) -> Any:
    #     items = [Sensors(**item) for item in items]
    #     self.session.add_all(items)
    #     return items

    # async def insert_all_sensors(self, items: list) -> Any:
    #     await self.session.execute(delete(self.model))

    #     query = insert(self.model).returning(self.model)
    #     res = await self.session.execute(query, items)
    #     logger.debug(f"{res = }")
    #     res = res.scalars().all()
    #     logger.debug(f"{res = }")
    #     res: list[Base] = [row.to_read_model() for row in res]
    #     logger.debug(f"{res = }")
    #     return res
    
        # ress = []
        # for data in items:
        #     stmt = insert(self.model).values(**data).returning(self.model.id)
        #     res = await self.session.execute(stmt)
        #     ress.append(res.scalar_one())
        # logger.debug(ress)
        # return ress

        # query = (insert(self.model).returning(self.model), items)
        # res = await self.session.execute(insert(self.model).returning(self.model), items)
        # res = res.scalars().all()
        # logger.debug(f"{res = }")
        # res: list[Base] = [row.to_read_model() for row in res]
        # logger.debug(f"{res = }")
        # return res


        # query = update(self.model)
        # res = await self.session.execute(query, items)




    # INSERT INTO sensors (id, sensor, type, device, pk_name) 
        # VALUES ($1::INTEGER, $2::VARCHAR, $3::VARCHAR, $4::VARCHAR, $5::VARCHAR) RETURNING sensors.id


        # await self.session.execute(delete(self.model))
    



        # query = select(self.model).filter(
        #     or_(
        #         self.model.id == 2615, 
        #         self.model.id == 2726
        #         )
        #     )
        # print(query.compile(compile_kwargs={"literal_binds": True}))

        # result = await self.session.execute(query)
        # res = result.scalars().all()
        # print(res)
        # res: list[DataBase_schema_sensor] = [row.to_read_model() for row in res]
        # print(res)
    
        # '''
        # query = delete(self.model).filter_by(id = data).returning(self.model.id)
        # query = delete(self.model).filter(self.model.id == data).returning(self.model.id)
        # '''
    
        # logger.warning(query.compile(compile_kwargs={"literal_binds": True}))



        # query = update(self.model).values(**data).filter_by(id = data["id"]).returning(self.model)
        # result = await self.session.execute(query)
        # model = result.scalar_one()
        # dto: Base_Model = model.to_read_model()
        # response = dto.model_dump()