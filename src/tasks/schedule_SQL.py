__all__ = ["DBScheduler_query"]

import json
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy import Insert, Select, delete, insert, select, update, and_, or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import CompilerElement
from sqlalchemy_celery_beat.session import ModelBase
from sqlalchemy_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, ModelMixin
from loguru import logger

from config import settings
from prtg.prtg_schema import Prtg_schema_historydata_input_OneDay
from tasks.tasks_schemas import Schema_add_PeriodicTask_Crontab, Schema_add_PeriodicTask_Interval, Schema_get_PeriodicTask, Schema_tasks_in, Schema_tasks_items



def print_stmt(stmt: CompilerElement):
    logger.debug(type(stmt))
    logger.debug(stmt.compile(compile_kwargs={"literal_binds": True}))


class DBScheduler_query:

    def __init__(self, session: Session):
        self.session = session


    def convert_sql_model(self, schema: BaseModel, res: list[ModelBase] | ModelBase): # type: ignore
        if isinstance(res, list):
            return [schema.model_validate(i, from_attributes=True).model_dump() for i in res]
        if isinstance(res, ModelBase):
            return schema.model_validate(res, from_attributes=True).model_dump()


    def get_one(self, model, id):
        return self.session.get(model, ident=id)
    

    def add_one(self, model, data):
        item = model(**data)
        self.session.add(item)
        self.session.flush()
        return item


    def update_one(self, item: ModelBase | ModelMixin, data): # type: ignore
        item.update(**data)
        '''flush отправляет запрос в базу данных, но не сохраняет окончательно'''
        self.session.flush()
        '''refresh нужен, если мы хотим заново подгрузить данные модели из базы'''
        self.session.refresh(item)
        return item

    
    def get_schedule_model(self, task_model,
        items: Schema_add_PeriodicTask_Crontab | Schema_add_PeriodicTask_Interval,
    ):
        if task_model == IntervalSchedule:
            kwargs = dict(every=items.every, period=items.period)
        else:
            kwargs = dict(
                minute = items.minute,
                hour = items.hour,
                day_of_week = items.day_of_week,
                day_of_month = items.day_of_month,
                month_of_year = items.month_of_year,
                timezone = settings.TIMEZONE
            )
        schedule = self.session.scalar(select(task_model).filter_by(**kwargs))
        if not schedule:
            schedule = self.add_one(task_model, kwargs)
        return schedule


                               
    '''Основные операции с задачами'''

    def get_periodic_tasks_all(self):
        res = self.session.scalars(select(PeriodicTask)).all()
        return self.convert_sql_model(Schema_get_PeriodicTask, res)


    def add_or_update_periodic_task(self, 
        # kwargs_task : Annotated[Schema_tasks_in, Depends()],
        items: Schema_add_PeriodicTask_Crontab | Schema_add_PeriodicTask_Interval,
        task_model = CrontabSchedule,
    ):
        schedule_model: IntervalSchedule | CrontabSchedule = self.get_schedule_model(task_model, items)
        periodic_task: PeriodicTask = self.session.scalar(select(PeriodicTask).filter_by(name=items.name))
        

        # auto_import_histor_args=json.dumps([day])
        auto_import_histor_kwargs = dict(hours=1, stime="08-00-00", etime="18-00-00")
        kwargs_task = json.dumps(auto_import_histor_kwargs)
        
        if not periodic_task:
            kwargs = dict(schedule_model = schedule_model, name = items.name, task = items.task, kwargs = kwargs_task)
            periodic_task = self.add_one(PeriodicTask, kwargs)
        else:
            kwargs = dict(schedule_id = schedule_model.id, task = items.task, enabled = items.enabled, kwargs = kwargs_task)
            periodic_task = self.update_one(periodic_task, kwargs)
        return self.convert_sql_model(Schema_get_PeriodicTask, periodic_task)


    def start_or_stop_list_periodic_tasks(self, enabled, id_list, model = PeriodicTask):
        stmt = update(model).values(enabled=enabled).filter(model.id.in_(id_list)).returning(model.id)
        res = self.session.scalars(stmt).all()
        return dict(enabled=enabled, data=res)


    def delete_rows(self, id_list: list, model: PeriodicTask | IntervalSchedule | CrontabSchedule):
        '''Удаляем график со всеми периодическими задачами, привязанными к нему'''
        stmt = select(model).filter(model.id.in_(id_list))
        result = self.session.scalars(stmt).all()        
        for i in result:
            self.session.delete(i)
        return result


        
        











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
    #     schedule = self.get_schedule_model(every)
    #     task = PeriodicTask(schedule_model = schedule, name = name, task = task)
    #     self.session.add(task)
    #     return task

    #     # data = dict(schedule_model = schedule, name = name, task = task)
    #     # query = insert(IntervalSchedule).values(**data).returning(IntervalSchedule)
    #     # result = self.session.execute(query)
    #     # model = result.scalar_one()
    #     # response = Schema_get_PeriodicTask.model_validate(model, from_attributes=True).model_dump()
    #     # return response
        

    # def get_periodic_tasks(self):
    #     # periodic_tasks
    #     model = IntervalSchedule
    #     join_model = PeriodicTask
    #     # query = (
    #     #     select(model, join_model.name, join_model.schedule_id)
    #     #     # .select_from(model)
    #     #     .join(join_model, model.id==join_model.schedule_id)
    #     #     # .join_from(model, join_model)
    #     #     # .where(join_model.schedule_id == model.id)

    #     #     # # .options(selectinload(PeriodicTask.schedule_model))
    #     #     # select(PeriodicTask.schedule_id, model.periodic_tasks)
    #     # )
    #     query = select(join_model)

    #     result = self.session.execute(query)
    #     res = result.scalars().all()
    #     for i in res:
    #         i.fff = i.schedule_model
    #     response = [i.__dict__ for i in res]

    #     # response = [i.__dict__ for i in res]
    #     # response = [i for i in res]
    #     # response = res
    #     # response = self.session.query(model.every, join_model.name).join(join_model, model.id==join_model.schedule_id).all()
    #     # logger.debug(response)


    #     # response: list[dict] = [i.__dict__ for i in res]
    #     # return response
    #     # response = [Schema_XXX.model_validate(i, from_attributes=True).model_dump() for i in res]
    #     logger.debug(response)

    #     return response        
        
    # def execute_in_py(self, models: list[Base] | Base):
    #     if isinstance(models, list):
    #         return [row.to_read_model().model_dump() for row in models]
    #     if isinstance(models, self.model):
    #         return models.to_read_model().model_dump()

    
    # def get_periodic_tasks(self):
    #     query = select(PeriodicTask)
    #     result = self.session.execute(query)
    #     res = result.scalars().all()
    #     response = [Schema_get_PeriodicTask.model_validate(i, from_attributes=True).model_dump() for i in res]
    #     # logger.debug(response)
    #     return response
    
    # def get_periodic_tasks(self):
    #     # result = self.session.query(PeriodicTask).all()
    #     result = self.session.scalars(select(PeriodicTask))
    #     res = result.all()
    #     logger.debug(res[0].schedule_model.__dict__)
    #     response: list[dict] = [i.__dict__ for i in res]
    #     return response        



    # def update_periodic_task(self, periodic_task, items: Schema_add_PeriodicTask_Interval):
    #     model = PeriodicTask
    #     schedule = self.get_schedule_model(items)

    #     data = dict(schedule_id = schedule.id, task=items.task, enabled=items.enabled)

    #     stmt = update(model).where(model.name == items.name).values(**data).returning(model.id)
    #     result = self.session.scalar(stmt)
    #     logger.debug(f"{result = }")
    #     logger.debug(f"{type(result) = }")

    #     # res = result.scalar_one()
    #     self.session.flush()

    #     # query = select(PeriodicTask).filter_by(name=items.name)
    #     # result = self.session.execute(query)
    #     # res = result.scalar_one_or_none()
    #     # response = Schema_get_PeriodicTask.model_validate(res, from_attributes=True).model_dump()
    #     # logger.success(response)
    #     # return response
    #     return self.get_one_periodic_tasks(model, id=result)
        

        '''-------------------------------------------------------------------------------------'''
        # def get_list_periodic_tasks(self, data):
        #     res = self.session.scalars(select(self.model).filter(self.model.id.in_(data))).all()
        #     return self.convert_sql_model(Schema_get_PeriodicTask, res)
        '''-------------------------------------------------------------------------------------'''

        '''-----------------------------------------------------------------------------------'''  
        # data = [{"id": i, "enabled" : enabled} for i in id_list]
        # self.session.execute(update(PeriodicTask), data)
        # return data
        '''-----------------------------------------------------------------------------------'''        
        # result = self.session.scalars(select(self.model).filter(self.model.id.in_(id_list)))
        # res = result.all()
        # for i in res:
        #     i.enabled = enabled
        # return self.convert_sql_model(res)
        '''-----------------------------------------------------------------------------------'''    
            # def delete_periodic_tasks(self, id_list):
        # result = self.session.get(PeriodicTask, ident=id)
        # logger.debug(result)
        # if result:
        #     self.session.delete(result)
        #     return {"status": True}
        # else:
        #     return {"status": False}
        '''-----------------------------------------------------------------------------------'''    
        # if not periodic_task:
            # task = PeriodicTask(schedule_model = schedule, name = items.name, task = items.task)
            # self.session.add(task)
            # insert_ata = dict(discriminator=schedule.discriminator, name = items.name, task = items.task)
            # self.session.execute(insert(PeriodicTask), insert_ata)        
        '''-----------------------------------------------------------------------------------'''    
        # def get_schedule_model(self, task_model, data):
        #     # data = dict(every=items.every, period=items.period)
        #     # query = select(IntervalSchedule).filter_by(**data)
        #     # result = self.session.execute(query)
        #     # schedule = result.scalar_one_or_none()
        #     # if not schedule:
        #     #     query = insert(IntervalSchedule).values(**data).returning(IntervalSchedule)
        #     #     result = self.session.execute(query)
        #     #     schedule = result.scalar_one()
        #     schedule = self.session.scalar(select(task_model).filter_by(**data))
        #     if not schedule:
        #         schedule = task_model(**data)
        #         self.session.add(schedule)
        #         self.session.flush()        
        #     return schedule    
        '''-----------------------------------------------------------------------------------'''    
        # def add_or_update_interval_task(self, items: Schema_add_PeriodicTask_Interval):
        #     periodic_task = self.session.scalar(select(PeriodicTask).filter_by(name=items.name))
        #     if not periodic_task:
        #         res = self.add_periodic_task(items)
        #     else:
        #         res = self.update_periodic_task(periodic_task, items)
        #     # PeriodicTaskChanged.update_from_session(self.session, False)
        #     return self.convert_sql_model(Schema_get_PeriodicTask, res)
        '''-----------------------------------------------------------------------------------'''    
        # stmt = delete(model).filter(model.id.in_(id_list)).returning(model.id)
        # return self.session.scalars(stmt).all()        
        '''-----------------------------------------------------------------------------------'''    