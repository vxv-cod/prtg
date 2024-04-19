from abc import ABC, abstractmethod
from typing import Type

from loguru import logger

from DataBase.db import async_session_maker
from DataBase.collections.db_models_repo import SensorsRepository, TypeSensorRepository, LoggingDownloadRepository, UserRepository
from DataBase.collections.db_models_repo import HistorydataRepository




class UnitOfWork:
    type_sensor = Type[TypeSensorRepository]
    sensors = Type[SensorsRepository]
    historydata = Type[HistorydataRepository]
    user_zgd = UserRepository(UserRepository)

        
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        logger.debug("DataBase: ON")
        self.session = self.session_factory()

        self.sensors = SensorsRepository(self.session)
        self.historydata = HistorydataRepository(self.session)
        self.type_sensor = TypeSensorRepository(self.session)
        self.logging_download = LoggingDownloadRepository(self.session)
        self.user_zgd = UserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()
        logger.debug("DataBase: END")

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


