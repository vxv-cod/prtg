import asyncio
import datetime
from typing import Annotated, Any
from pydantic import BaseModel
from sqlalchemy import ForeignKey, and_, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from rich import print
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import  async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from sqlalchemy.orm import relationship, joinedload, subqueryload
from sqlalchemy import String, create_engine
from sqlalchemy import func


from pydantic import BaseModel


intpk = Annotated[int, mapped_column(primary_key=True)]
strpk = Annotated[str, mapped_column(primary_key=True)]

PRTG_SERVER = "http://10.28.70.200"
DEBUG = True
USER = "vxv"
PASWORD = 1234  # pgAdmin 4
PASSHASH = 3751896299

DataBase_HOST="localhost"
DataBase_PORT=5454
DataBase_NAME="demo_01"
DataBase_USER="postgres"
DataBase_PASS="postgres"

async_engine = create_async_engine(
    # url=Settings.DATABASE_URL,
    url=f"postgresql+asyncpg://{DataBase_USER}:{DataBase_PASS}@{DataBase_HOST}:{DataBase_PORT}/{DataBase_NAME}",
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine)


sync_engine = create_engine(
    url=f"postgresql+asyncpg://{DataBase_USER}:{DataBase_PASS}@{DataBase_HOST}:{DataBase_PORT}/{DataBase_NAME}",
    echo=True,
)
session_factory = sessionmaker(sync_engine)



class Base(DeclarativeBase):
    '''Если указать схему, то ее нужно прописывать перед названием таблицы в колонках'''
    # __table_args__ = {"schema": "stack"}
    pydantic_schema : BaseModel = None
    id : int
    def to_read_model(self) -> pydantic_schema:
        return self.pydantic_schema.model_validate(self.__dict__, from_attributes=True)
    
    # def __repr__(self) -> str:
    #     xxx = self.__dict__.copy()
    #     xxx.pop('_sa_instance_state')
    #     return f"{xxx}"


class Base_Model(BaseModel):
    id : int | str
    class Config:
        from_attributes = True  


class Schema_type_sensor(Base_Model):
    id: int
    type: str
    value: str


class Schema_Sensors(Base_Model):
    id: int
    type_id: int
    pk_name: str
    

class schema_type_and_Sensors(Schema_type_sensor):
    sensors : list[Schema_Sensors]



class Sensors_schema_m2o(Schema_Sensors):
    type_sensor : Schema_type_sensor

    

class Sensors(Base):
    __tablename__ = "sensors"

    pydantic_schema = Schema_Sensors
    id: Mapped[intpk]
    type_id: Mapped[int] = mapped_column(ForeignKey("type_sensor.id", ondelete="CASCADE"))
    pk_name: Mapped[str]

    type_sensor: Mapped["TypeSensor"] = relationship(back_populates="sensors")




class TypeSensor(Base):
    __tablename__ = "type_sensor"
    pydantic_schema = Schema_type_sensor

    id: Mapped[intpk]
    type: Mapped[str]
    value: Mapped[str]

    sensors: Mapped[list["Sensors"]] = relationship(back_populates="type_sensor")



class Schema_historydata(Base_Model):
    id: str = "str_date - sensor_id"
    date: datetime.date
    pk_name: str = "pk_name"
    sensor_id: int | None = None
    type_id: int | None = None

    
class Historydata(Base):
    __tablename__ = "historydata"
    pydantic_schema = Schema_historydata

    id: Mapped[strpk]
    date: Mapped[datetime.date]
    pk_name: Mapped[str]
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id", ondelete="CASCADE"))
    type_id: Mapped[int] = mapped_column(ForeignKey("type_sensor.id", ondelete="CASCADE"))

    min_value : Mapped[float]
    avg_value : Mapped[float]
    max_value : Mapped[float]



def sql_in_py(schema, data):
    return [schema.model_validate(i, from_attributes=True).model_dump() for i in data]


def dto_in_py(models: list[Base] | Base):
    if isinstance(models, list):
        return [row.to_read_model().model_dump() for row in models]
    else:
        return models.to_read_model().model_dump()
        




async def select_mTo_or_oTo():
    async with async_session_factory() as session:
        model = Sensors
        query = (
            select(model)
            .options(joinedload(model.type_sensor))
        )
        res = await session.execute(query)
        result = res.unique().scalars().all()
        
        dto = sql_in_py(Sensors_schema_m2o, result)
        print(dto[0])




async def select_oTm_or_mTm():
    async with async_session_factory() as session:
        model = TypeSensor
        query = (
            select(model)
            .options(selectinload(model.sensors))
        )
        
        res = await session.execute(query)
        result = res.scalars().all()
        print(dto_in_py(result))

        # dto = sql_in_py(schema_type_and_Sensors, result)
        # print(dto[0])

        worker_1_resumes = result[0].sensors[:2]
        print(dto_in_py(worker_1_resumes))



async def select_contains_eager():
    '''Данная конструкция позволяет отсортировать значения'''
    async with async_session_factory() as session:
        model = TypeSensor
        query = (
            select(model)
            .join(model.sensors)
            .options(contains_eager(model.sensors))
            # .filter(Sensors.pk_name == 'H73Z9Q2')
        )

        res = await session.execute(query)
        result = res.unique().scalars().all()
        print("result =", result)
        # print("dto_in_py =", dto_in_py(result))

        # worker_1_resumes = result[0].sensors[:2]
        # print("dto_in_py =", dto_in_py(worker_1_resumes))
        
        # dto = sql_in_py(schema_type_and_Sensors, result)
        # print(dto[:2])








# class Sensors_schema_m2o_select_m2o_test(Schema_sensor):
#     type_sensor : Schema_type_sensor.type


class Select_join_from(Base_Model):
    id: int
    type_id: int
    pk_name: str
    # type: str
    typeSensor_type: str

async def select_join_from():
    '''Можно указать левую и правую часть подгрузки'''
    async with async_session_factory() as session:
        query = (
            select(Sensors.id, Sensors.pk_name, Sensors.type_id, TypeSensor.type.label("typeSensor_type"))
            .join_from(Sensors, TypeSensor)
        )
        res = await session.execute(query)
        result = res.all()[:10]
        dto = sql_in_py(Select_join_from, result)
        print(dto)



# class Select_join(Base_Model):
#     id: int
#     type_id: int
#     # pk_name: str
#     type: str



class Select_join(Base_Model):
    id: int
    type_id: int
    type: str
    pk_name: str

async def select_join():
    '''Можно указать только правую часть подгрузки'''
    async with async_session_factory() as session:
        query = (
            select(Sensors.id, Sensors.pk_name, Sensors.type_id, TypeSensor.type)
            .join(TypeSensor)
        )
        res = await session.execute(query)
        result = res.all()[:10]
        dto = sql_in_py(Select_join, result)
        print(dto)





class Sselect_join_historydata(Base_Model):
    id: str
    # date: datetime.date
    historydata_pk_name: str
    type_id: int
    type: str
    sensor_id: int
    sensors_table_id: int


# async def select_join_historydata():
#     '''Можно указать только правую часть подгрузки'''
#     async with async_session_factory() as session:
#         query = (
#             select(
#                 Historydata.id, 
#                 Historydata.pk_name.label("historydata_pk_name"), 
                
#                 Historydata.type_id, 
#                 TypeSensor.type, 
                
#                 Historydata.sensor_id, 
#                 Sensors.id.label("sensors_table_id")
#             )
#             # .join_from(Historydata, TypeSensor)
#                 # .join(TypeSensor)
#                 # .join(Sensors)
#             .join((TypeSensor, Sensors))

#         )
#         res = await session.execute(query)
#         result = res.all()[:10]
#         dto = sql_in_py(Sselect_join_historydata, result)
#         print(dto)


async def select_order_by():
    async with async_session_factory() as session:
        query = (
            select(Sensors)
            .order_by(Sensors.type_id)
        )
        res = await session.execute(query)
        result = res.scalars().all()[:10]
        dto = sql_in_py(Schema_Sensors, result)
        print(dto)        




class Schema_group_by(Base_Model):
    # date: datetime.date
    # id: int
    # type_id: int
    type: str

    count: int


async def select_group_by():
    async with async_session_factory() as session:
        query = (
            select(
                TypeSensor.type.label("type").cast(String),
                func.count(Sensors.id).label("count"),
            )
            .join(Sensors)
            .group_by(TypeSensor.type)
        )
        res = await session.execute(query)
        result = res.all()
        result = dict(result)
        print(result)




if __name__ == "__main__":
    # funcgo = select_workers_with_joined_relationship()
    # funcgo = select_workers_with_selectin_relationship()
    # funcgo = select_workers_with_condition_relationship_contains_eager()
    # funcgo = select_m2o()
    # funcgo = select_contains_eager()
    # funcgo = select_mTo_or_oTo()
    # funcgo = select_join_from()
    # funcgo = select_join()
    # funcgo = select_order_by()
    funcgo = select_group_by()

    asyncio.run(funcgo)


    # count_fn()
        
    # from sqlalchemy import func
    # count_fn = func.count(Sensors.id)
    # print(f"{count_fn = }")

    ...


