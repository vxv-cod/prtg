# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     PRTG_SERVER: str
#     DEBUG: bool
#     USER: str
#     PASWORD: str
#     PASSHASH: str
    
#     DataBase_HOST: str
#     DataBase_PORT: int
#     DataBase_USER: str
#     DataBase_PASS: str
#     DataBase_NAME: str

#     REDIS_URL: str

#     # @property
#     # def PRTG_SERVER(self):
#     #     return f'{self.PRTG_SERVER}'

#     @property
#     def DATABASE_URL(self):
#         # sqlite+aiosqlite:///sqlite.DataBase
#         # return f"sqlite+aiosqlite:///sqlite.DataBase"
#         return f"postgresql+asyncpg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
#         # return f"postgresql+psycopg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
#         # return f"postgresql+psycopg2://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
#         # return f"cockroachDataBase+asyncpg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
    

#     # @property
#     # def DATABASE_URL_async_pg(self):
#     #     # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
#     #     return f"postgresql+asyncpg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
    
#     model_config = SettingsConfigDict(env_file="src\.env")

# settings = Settings()

import os
from dotenv import load_dotenv
load_dotenv()



class Settings:
    def __init__(self) -> None:
        self.PRTG_SERVER: str = os.getenv("PRTG_SERVER")
        self.DEBUG: bool = os.getenv("DEBUG")
        self.USER: str = os.getenv("USER")
        self.PASWORD: str = os.getenv("PASWORD")
        self.PASSHASH: str = os.getenv("PASSHASH")
        
        self.DataBase_HOST: str = os.getenv("DataBase_HOST")
        self.DataBase_PORT: int = os.getenv("DataBase_PORT")
        self.DataBase_USER: str = os.getenv("DataBase_USER")
        self.DataBase_PASS: str = os.getenv("DataBase_PASS")
        self.DataBase_NAME: str = os.getenv("DataBase_NAME")
        self.DATABASE_URL_ASUNC: str = f"postgresql+asyncpg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
        self.DATABASE_URL_SUNC: str = f"postgresql+psycopg2://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
        
        self.REDIS_URL: str = os.getenv("REDIS_URL")
        self.TIMEZONE: str = os.getenv("TIMEZONE")
        self.BEAT_DBURL: str = os.getenv("BEAT_DBURL")
        self.BEAT_RESULT: str = os.getenv("BEAT_RESULT")
        self.FLOWER_PORT: str = os.getenv("FLOWER_PORT")


settings = Settings()