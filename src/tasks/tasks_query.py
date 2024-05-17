__all__ = ["DBScheduler_query"]

from typing import Any
from pydantic import BaseModel
from sqlalchemy import Insert, Select, delete, insert, select, update, and_, or_
from sqlalchemy.orm import Session

from sqlalchemy_celery_beat.models import PeriodicTask, IntervalSchedule, Period, PeriodicTaskChanged
from sqlalchemy_celery_beat import schedulers
from sqlalchemy_celery_beat.session import SessionManager, session_cleanup
from loguru import logger
from tasks.celery_app import celery_app

from tasks.schemas import Schema_get_PeriodicTask



# class PeriodicTask(PeriodicTask):
#     pydantic_schema = Schema_get_PeriodicTask
    
#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         super().__init__(*args, **kwargs)
    
#     def to_read_model(self):
#         return self.pydantic_schema.model_validate(self.__dict__, from_attributes=True).model_dump()   




class DBScheduler_query:
    def __init__(self, session: Session):
        self.session = session

    # def execute_in_py(self, models: list[Base] | Base):
    #     if isinstance(models, list):
    #         return [row.to_read_model().model_dump() for row in models]
    #     if isinstance(models, self.model):
    #         return models.to_read_model().model_dump()

    
    def get_periodic_tasks(self):
        query = select(PeriodicTask)
        result = self.session.execute(query)
        res = result.scalars().all()
        response = [Schema_get_PeriodicTask.model_validate(i, from_attributes=True).model_dump() for i in res]
        logger.debug(response)
        return response
        

    def add_schedule(self, every: int):
        data = dict(every=every, period=Period.SECONDS)
        query = select(IntervalSchedule).filter_by(**data)
        result = self.session.execute(query)
        schedule = result.scalar_one_or_none()
        if not schedule:
            query = insert(IntervalSchedule).values(**data).returning(IntervalSchedule)
            result = self.session.execute(query)
            schedule = result.scalar_one()
        return schedule



    def add_periodic_task(self, name, task, every):
        schedule = self.add_schedule(every)
        data = dict(schedule_model = schedule, name = name, task = task)
        periodic_task = PeriodicTask(**data)
        self.session.add(periodic_task)
        
        return periodic_task



       # tasks.service.add_test_task


    def update_periodic_task(self, name, data):
        stmt = update(PeriodicTask).where(PeriodicTask.name == name).values(**data).returning(PeriodicTask)
        result = self.session.execute(stmt)
        res = result.scalar_one()
        response = Schema_get_PeriodicTask.model_validate(res, from_attributes=True).model_dump()
        logger.debug(f"{res = }")

        logger.success(response)
        return response


    def add_or_update_periodic_task(self, name, task, every, enabled):
        query = select(PeriodicTask).filter_by(name=name)
        result = self.session.execute(query)
        periodic_task = result.scalar_one_or_none()
        data = dict(name=name, task=task, every=every)
        if not periodic_task:
            logger.warning("not")
            res = self.add_periodic_task(**data)
        else:
            schedule = self.add_schedule(every)
            data = dict(schedule_id = schedule.id, task=task, enabled=enabled)
            res = self.update_periodic_task(name, data)
        PeriodicTaskChanged.update_from_session(self.session, False)
        return res


    def stop_periodic_tasks(self, id):
        '''-------------------------------------------------------------------------------'''
        task = self.session.get_one(PeriodicTask, id)
        task.enabled = False
        return task
        '''-------------------------------------------------------------------------------'''
        # query = update(PeriodicTask).filter_by(name=name).values(enabled=0).returning(PeriodicTask)
        # result = self.session.execute(query)
        # res = result.scalar_one()
        # response = Schema_get_PeriodicTask.model_validate(res, from_attributes=True).model_dump()
        # PeriodicTaskChanged.update_from_session(self.session, 0)
        # return response
        '''-------------------------------------------------------------------------------'''

    # def delete_periodic_tasks(self, name):
        # query = delete(PeriodicTask).filter(PeriodicTask.name == name).returning(PeriodicTask)
        # result = self.session.execute(query)
        # res = result.scalar_one()
        # logger.debug(res.__dict__)
        # response = Schema_get_PeriodicTask.model_validate(res, from_attributes=True).model_dump()
        # # PeriodicTaskChanged.update_from_session(self.session, False)
        # return response

    def delete_periodic_tasks(self, id):
        task = self.session.get_one(PeriodicTask, ident=id)
        self.session.delete(task)
        return task

        ...
        # logger.debug(celery_app.Beat().Service)
        # from celery.beat import Service
        # xxxx = Service(celery_app).scheduler
        # logger.debug(xxxx)
        # PeriodicTaskChanged.update_from_session(self.session, 1)

        # return task


        # query = delete(PeriodicTask).filter_by(name=name).returning(PeriodicTask)
        # result = self.session.execute(query)
        # res = result.scalar_one_or_none()
        # return res
        

        # PeriodicTask(name=name)






        # task = self.session.get(PeriodicTask, ident={id})
        # self.session.delete(task)
        # PeriodicTaskChanged.update_from_session(self.session, 0)




        # task = self.session.query(PeriodicTask).filter(PeriodicTask.name==name).first()
        # task = PeriodicTask(name="test", task="tasks.service.add_test_task", schedule_id=13)

        # self.session.add(task)
        # # self.session.add(task)
        # # self.session.commit()

        # logger.debug(task)
        # self.session.delete(task)
        # # logger.debug(task)
        # self.session.flush()
        # return task
    





    # def add_periodic_task(self, name, task, every):
    #     schedule = self.add_schedule(every)
    #     task = PeriodicTask(schedule_model = schedule, name = name, task = task)
    #     self.session.add(task)
    #     return task

    #     # data = dict(schedule_model = schedule, name = name, task = task)
    #     # query = insert(IntervalSchedule).values(**data).returning(IntervalSchedule)
    #     # result = self.session.execute(query)
    #     # model = result.scalar_one()
    #     # response = Schema_get_PeriodicTask.model_validate(model, from_attributes=True).model_dump()
    #     # return response