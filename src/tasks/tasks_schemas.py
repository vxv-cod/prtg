import datetime
from enum import Enum, StrEnum, auto
from typing import Any
from loguru import logger
from pydantic import BaseModel, Field, Json, computed_field, model_validator

# from .basemodel import Base_Model
from sqlalchemy_celery_beat.models import PeriodicTask, IntervalSchedule, Period, PeriodicTaskChanged, CrontabSchedule


# from tasks.celery_app import celery_app
from config import settings
from prtg.prtg_schema import Prtg_schema_historydata_input
from tasks.tasks_enum import EnumTasks_task


class Base_Model(BaseModel):
    class Config:
        from_attributes = True 
    ...

class Schema_BaseModel(BaseModel):
    id: int


class Schema_beat_schedule(BaseModel):
    schedule: int
    task: str
    args: str | list
    kwargs: Json

    @model_validator(mode='after')
    def valid(self):
        if isinstance(self.args, str):
            obj = [i.strip(" ") for i in self.args.split(",")]
            new = []
            for i in obj:
                try: new.append(float(i))
                except: new.append(i)
            self.args = new
        return self



class Schema_tasks_in(Prtg_schema_historydata_input):
    sdate: datetime.date = Field(exclude=True, default=datetime.datetime.now().date() - datetime.timedelta(days=1))
    edate: datetime.date = Field(exclude=True, default=datetime.datetime.now().date() - datetime.timedelta(days=1))

    @computed_field
    def list_days(self) -> list[datetime.date]:
        '''Вычисляемой поле (спикок дат)'''
        # count_days: datetime.timedelta = (self.edate - self.sdate)
        return [self.sdate + datetime.timedelta(days=i) for i in range(self.count_days)]   
    
    
class Schema_task_kwargs(BaseModel):
    hours: int
    stime: str
    etime: str


class Schema_tasks_items(BaseModel):
    list_days: list[datetime.date]
    kwargs: Schema_task_kwargs
    
    @model_validator(mode='before')
    @classmethod
    def check_input_data(cls, data: dict) -> Any:
        '''data - входные данные'''
        data["list_days"] = data.pop("list_days")
        data["kwargs"] = data
        return data


    

# class Schema_CelerySchedule(BaseModel):
#     # id: int
#     name: str = "task_for_every_day"
#     schedule: int = 5 # Интервал в секундах
#     task: str = "schedule_task"
#     args: str | None = None
#     kwargs: str | None = None
    
    # task_name: str
    # task_args: str
    # task_kwargs: str
    # schedule: int  # Интервал в секундах
    # last_run = datetime.datetime




# class Schema_CrontabSchedule(BaseModel):
#     # id: int
#     minute: str = '0'
#     hour: str = '1'
#     day_of_week: str = '*'
#     day_of_month: str = '*'
#     month_of_year: str = '*'
#     timezone: str = settings.TIMEZONE

class Schema_CrontabSchedule_query(Base_Model):
    minute: str | None = "*"
    hour: str | None = "*"
    day_of_week: str | None = "*"
    day_of_month: str | None = "*"
    month_of_year: str | None = "*"




class Schema_IntervalSchedule_query(Base_Model):
    every: int
    period: Period = Period.SECONDS



# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# class EnumTasks(str, Enum):
#     add_task_manual = "tasks.service.add_task_manual"
#     add_test_task = "tasks.service.add_test_task"




# from tasks.celery_app import celery_app
# def get_all_task_name():
#     tasks: dict = celery_app._tasks
#     res = list(tasks.keys())
#     res_dict = [(i.split(".")[-1], i) for i in res]
#     return res_dict

# from tasks.tasks_repo import TasksRepository


# EnumTasks_task = StrEnum(
#     value="EnumTasks_task",
#     names=(TasksRepository.get_all_task_name()),
#     # start=auto()

# )





# class EnumTasks_task(xxxx, str ):
#     ...


class Schema_PeriodicTask_query(Base_Model):
    name: str = "test"
    # task: EnumTasks_task | str = EnumTasks_task.add_test_task
    # task: EnumTasks_task | str
    task: EnumTasks_task
    enabled: bool = True
    # args: str | None = None
    # kwargs: str | None = None



'''Запрос данных'''
'''--------------------------------------------------------------------------------'''
class Schema_add_PeriodicTask_Interval(Schema_IntervalSchedule_query, Schema_PeriodicTask_query):
    ...

class Schema_add_PeriodicTask_Crontab(Schema_CrontabSchedule_query, Schema_PeriodicTask_query):
    ...


'''Обработка результатов данных'''
'''--------------------------------------------------------------------------------'''
class Schema_IntervalSchedule(Schema_IntervalSchedule_query, Schema_BaseModel):
    ...

class Schema_CrontabSchedule(Schema_CrontabSchedule_query, Schema_BaseModel):
    timezone: str

class Schema_get_PeriodicTask(Schema_PeriodicTask_query, Schema_BaseModel):
    discriminator: str
    schedule_id: int
    schedule_model: Schema_CrontabSchedule | Schema_IntervalSchedule
'''--------------------------------------------------------------------------------'''




class Schema_update(Base_Model):
    id: int
    name: str
    enabled: bool






# class Ssssssss(Base_Model):
#     name: str = "test"
#     task: EnumTasks_task | str = EnumTasks_task.add_test_task
#     enabled: bool = True
#     discriminator: str
#     schedule_id: int
#     schedule_model: Schema_CrontabSchedule | Schema_IntervalSchedule



    # id: int = Field(exclude=True)


    # @model_validator(mode='after')
    # def validic(self):
    #     if isinstance(self.schedule_model, IntervalSchedule):
    #         logger.debug(self.discriminator)
    #         if self.discriminator == "intervalschedule":
    #             # self.schedule_model = Type[Schema_IntervalSchedule]
    #             self.schedule_model = Schema_IntervalSchedule.model_validate(self.schedule_model, from_attributes=True).model_dump()
    #         else:
    #             self.schedule_model = Schema_CrontabSchedule
    #     return self 
        # self.schedule_model = Type[Schema_IntervalSchedule]
        # logger.debug(f"{self.schedule_model = }")
        # return self 


    # @model_validator(mode='before')
    # @classmethod
    # def check_input_data(cls, data) -> Any:
    #     if data.discriminator == "intervalschedule":
    #         data.discriminator = Schema_IntervalSchedule.model_validate(data.discriminator, from_attributes=True)
    #     else:
    #         data.discriminator = Schema_CrontabSchedule.model_validate(data.discriminator, from_attributes=True)
    #     # return cls             
    #     return data

