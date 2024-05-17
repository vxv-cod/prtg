from typing import Any
import datetime

from pydantic import BaseModel, Field, computed_field, model_validator
from loguru import logger
from DataBase.schemas.historydata import DataBase_schema_historydata

from DataBase.schemas.sensors import DataBase_schema_sensor



def string_to_datetime(string: str, format: str = '%d.%m.%Y %H:%M:%S') -> datetime.datetime:
    ''' Преобразуем строку в dateime в строку 
    format_example = %d.%m.%Y %H:%M:%S '''
    return datetime.datetime.strptime(string, format)


class Prtg_schema_import_in_DB_id_Int(BaseModel):
    insert_list : list[int]
    update_list : list[int]

class Prtg_schema_import_in_DB_historydata(BaseModel):
    date : datetime.date
    count: int
    insert_list : list[str]
    update_list : list[str]


class Prtg_schema_Sensor(DataBase_schema_sensor):
    id: int = Field(validation_alias='objid')





class Prtg_schema_historydata_input(BaseModel):
    hours: int = 1
    stime: str = '08-00-00'
    etime: str = '18-00-00'
    sdate: str | datetime.date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    edate: str | datetime.date = datetime.datetime.now().date() - datetime.timedelta(days=1)

    @model_validator(mode='after')
    def valid(self):
        '''Проверка времени'''
        stime_datetime = datetime.datetime.strptime(self.stime, "%H-%M-%S")
        etime_datetime = datetime.datetime.strptime(self.etime, "%H-%M-%S")
        if etime_datetime < stime_datetime:
            self.etime = self.stime
        '''Проверка начальной и конечной даты'''
        # logger.debug(f"{type(self.sdate) = }")
        if isinstance(self.sdate, str):
            self.sdate = datetime.datetime.strptime(self.sdate, '%Y-%m-%d').date()
        if isinstance(self.edate, str):
            self.edate = datetime.datetime.strptime(self.edate, '%Y-%m-%d').date()            
        min_date = min(self.sdate, self.edate)
        max_date = max(self.sdate, self.edate)
        self.sdate = min_date
        self.edate = max_date            
        return self            

    @computed_field
    def count_days(self) -> int:
        '''Вычисляемой поле (разница дат)'''
        res: datetime.timedelta = (self.edate - self.sdate)
        return res.days + 1



class Schema_tasks_in(Prtg_schema_historydata_input):
    sdate: datetime.date = Field(exclude=True, default=datetime.datetime.now().date() - datetime.timedelta(days=1))
    edate: datetime.date = Field(exclude=True, default=datetime.datetime.now().date() - datetime.timedelta(days=1))

    @computed_field
    def list_days(self) -> list[datetime.date]:
        '''Вычисляемой поле (спикок дат)'''
        # count_days: datetime.timedelta = (self.edate - self.sdate)
        return [self.sdate + datetime.timedelta(days=i) for i in range(self.count_days)]    


class Schema_tasks_out(BaseModel):
    hours: int
    stime: str
    etime: str
    # day: list[datetime.date]


class Prtg_schema_historydata_calculations(DataBase_schema_historydata):
    '''Данная схема приводит данные к виду DB'''
    @classmethod
    def list_mma(cls, stime, etime, histdata_dict : list[dict[str, Any]], search : str):
        def convert_time(string: str):
            time_obj: str = string.split(' ')
            str_date: str = time_obj[0].rjust(10, '0')
            str_date = datetime.datetime.strptime(str_date, '%d.%m.%Y').strftime('%Y.%m.%d')
            str_time: str = time_obj[1].rjust(8, '0')
            str_data_time = f"{str_date} {str_time}"
            return str_data_time, str_date
        
        total_list = []
        for obj in histdata_dict:
            str_data_time, str_date = convert_time(obj["datetime"])
            
            date_time_obj = string_to_datetime(str_data_time, format='%Y.%m.%d %H:%M:%S')
            format: str = '%Y.%m.%d %H-%M-%S'
            stime_obj_datatime = string_to_datetime(f"{str_date} {stime}", format=format)
            etime_obj_datatime = string_to_datetime(f"{str_date} {etime}", format=format)

            if stime_obj_datatime <= date_time_obj <= etime_obj_datatime:
                val = obj[search]
                val = 0 if val == '' else val
                if val != 0 or val != '':
                    total_list.append(val)
    
        return total_list, str_date
    
    @model_validator(mode='before')
    @classmethod
    def check_input_data(cls, data: dict) -> Any:
        '''
        Данная схема получает одни данные, а выдает другие, из за этого используем' @model_validator(mode='before')
        для обработки сырых данных и формировании класса ответа.
        '''
        stime: str = data["stime"]
        etime: str = data["etime"]
        total_list = []
        histdata_dict = data['histdata']

        if data['type_id'] == 0:
            sre_date_time = cls.list_mma(stime, etime, histdata_dict, "Всего")
        if data['type_id'] == 1:
            sre_date_time = cls.list_mma(stime, etime, histdata_dict, "Свободное пространство")
        if data['type_id'] == 2:
            sre_date_time = cls.list_mma(stime, etime, histdata_dict, "Процент доступной памяти")
        
        [total_list, str_date] = sre_date_time
        
        data["date"] : str = datetime.datetime.strptime(str_date, '%Y.%m.%d')
        data["id"] : str = f"{str_date} - {data['sensor_id']}"
        if total_list != []:
            data["max_value"] : float = round(max(total_list), 4)
            data["avg_value"] : float = 0 if len(total_list) == 0 else round(sum(total_list)/len(total_list), 4)
            data["min_value"] : float = round(min(total_list), 4)
        
        return data
    
class Prtg_schema_historydata_headers(BaseModel):
    sensor_id: int | None = None
    type_id: int | None = None
    pk_name: str | None = None
    stime: str | None = None
    etime: str | None = None
    histdata: list = []


'''Примеры кода'''
# from pydantic import BaseModel, Field, field_validator
# from typing_extensions import Annotated


# class Historydata_schema_one(BaseModel):
#     datetime: str
#     # Всего: str
#     CPU: float | None = Field(validation_alias="Всего", default=None)
#     Memory: float | None = Field(validation_alias="Процент доступной памяти", default=None)
#     HDD: float | None = Field(validation_alias="Свободное пространство", default=None)

#     # @field_validator(*['CPU', 'Memory', 'HDD'])
#     # @classmethod
#     # def valid(cls, v: Any):
#     #     if v == "":
#     #         return None

# class Historydata_schema_one_test(BaseModel):
#     datetime: str
#     medium: float = 0.0

#     CPU: Any = Field(validation_alias="Всего", default='')
#     Memory: Any = Field(validation_alias="Процент доступной памяти", default='')
#     HDD: Any = Field(validation_alias="Свободное пространство", default='')

#     @model_validator(mode='after')
#     def valid(self):
#         '''Изменяем поле "medium" на значение полей [CPU, Memory, HDD] с удалением самих после '''
#         for k, v in self:
#             if k not in ['datetime', 'medium']:
#                 if v != '':
#                     self.__setattr__("medium", v)
#                 self.__delattr__(k)

#         return self


    # @field_validator(*['CPU', 'Memory', 'HDD'])
    # @classmethod
    # def valid(cls, v: Any):
    #     if v == "":
    #         return None