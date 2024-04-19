from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PRTG_SERVER: str
    DEBUG: bool
    USER: str
    PASWORD: str
    PASSHASH: str
    
    DataBase_HOST: str
    DataBase_PORT: int
    DataBase_USER: str
    DataBase_PASS: str
    DataBase_NAME: str

    # @property
    # def PRTG_SERVER(self):
    #     return f'{self.PRTG_SERVER}'

    @property
    def DATABASE_URL(self):
        # sqlite+aiosqlite:///sqlite.DataBase
        # return f"sqlite+aiosqlite:///sqlite.DataBase"
        return f"postgresql+asyncpg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
        # return f"postgresql+psycopg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
        # return f"postgresql+psycopg2://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
        # return f"cockroachDataBase+asyncpg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
    

    # @property
    # def DATABASE_URL_async_pg(self):
    #     # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
    #     return f"postgresql+asyncpg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
    
    model_config = SettingsConfigDict(env_file="src\.env")

settings = Settings()
