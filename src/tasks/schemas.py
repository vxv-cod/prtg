import datetime
from typing import Any
from pydantic import BaseModel, Json, model_validator
from sqlalchemy import DateTime
# from .basemodel import Base_Model


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



class Schema_CelerySchedule(BaseModel):
    # id: int
    name: str = "task_for_every_day"
    schedule: int = 5 # Интервал в секундах
    task: str = "schedule_task"
    args: str | None = None
    kwargs: str | None = None
    
    # task_name: str
    # task_args: str
    # task_kwargs: str
    # schedule: int  # Интервал в секундах
    # last_run = datetime.datetime


class Schema_add_PeriodicTask(BaseModel):
    name: str = "test"
    task: str = "tasks.service.add_test_task"
    every: int = 1
    enabled: bool = True

    
class Schema_get_PeriodicTask(BaseModel):
    id: int
    name: str
    discriminator: str
    schedule_id: int
    enabled: bool = 1
    last_run_at: datetime.datetime | None
    