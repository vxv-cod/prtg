import datetime
from loguru import logger

from pydantic import model_validator
from .basemodel import Base_Model



def string_to_datetime(string: str, format: str = '%Y-%m-%d') -> datetime.datetime:
    ''' Преобразуем dateime в строку 
    format_example = %d.%m.%Y %H:%M:%S '''
    return datetime.datetime.strptime(string, format)

def datetime_to_string(date_time: datetime.datetime, format: str = '%Y-%m-%d') -> str:
    ''' Преобразуем строку в dateime
    format_example = %d.%m.%Y %H:%M:%S '''
    return date_time.strftime(format)



class DataBase_schema_historydata(Base_Model):
    id: str = "str_date - sensor_id"
    
    zgd_id: int | None = None
    division_id: int | None = None
    
    date: datetime.date
    pk_name: str = "pk_name"
    sensor_id: int | None = None
    type_id: int | None = None
    
    min_value : float = 0
    avg_value : float = 0
    max_value : float = 0



class DB_schema_Log_hist_in(Base_Model):
    id: str | datetime.date = datetime.datetime.now().date().isoformat()
    count_sensors: int
    status: bool

    @model_validator(mode='after')
    def valid(self):
        # logger.warning(type(self.date_of_the_data))
        '''Работа с полученным экземпляром входных данных'''
        if isinstance(self.id, str):
            self.id = datetime.datetime.strptime(self.id, '%Y-%m-%d').date()
            logger.debug(f"{self.id} {type(self.id)}")

        return self


class DB_schema_Log_hist_out(DB_schema_Log_hist_in):
    created_at: datetime.datetime
    updated_at: datetime.datetime
