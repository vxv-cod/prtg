from loguru import logger
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

sync_engine = create_engine(url=settings.DATABASE_URL_SUNC)
# sync_engine.echo = True
sync_session_maker = sessionmaker(bind=sync_engine)

async_engine = create_async_engine(settings.DATABASE_URL_ASUNC)
# async_engine.echo = settings.DEBUG
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    '''Если указать схему, то ее нужно прописывать перед названием таблицы в колонках'''
    # __table_args__ = {"schema": "stack"}
    pydantic_schema : BaseModel = None
    id : int
    def to_read_model(self) -> BaseModel:
        return self.pydantic_schema.model_validate(self.__dict__, from_attributes=True)



