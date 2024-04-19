from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


engine = create_async_engine(settings.DATABASE_URL)
# engine.echo = settings.DEBUG

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    '''Если указать схему, то ее нужно прописывать перед названием таблицы в колонках'''
    # __table_args__ = {"schema": "stack"}
    pydantic_schema : BaseModel = None
    id : int
    def to_read_model(self) -> pydantic_schema:
        return self.pydantic_schema.model_validate(self.__dict__, from_attributes=True)



