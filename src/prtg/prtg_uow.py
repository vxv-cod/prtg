from abc import ABC, abstractmethod
from typing import Type

import httpx
from loguru import logger

from prtg.prtg_repository import PrtgRepository


        
class Prtg_UOW:
    query = Type[PrtgRepository]
    CLIENT_PARAMS = {
        "trust_env" : False, 
        "verify" : False, 
        "timeout" : httpx.Timeout(timeout=None),
        }
    
    def __init__(self):
        self.client_factory = httpx.AsyncClient
    
    async def __aenter__(self):
        logger.debug("Клиент открыт")
        '''Создаем экземпляр клиента (сессии соединения с сервером)'''
        self.client = self.client_factory(**self.CLIENT_PARAMS)
        self.query = PrtgRepository(client=self.client)

    async def __aexit__(self, *args):
        await self.client.aclose()
        logger.debug("Клиент закрыт")
