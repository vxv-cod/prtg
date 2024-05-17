
import datetime
from typing import Any
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase

from DataBase.db import Base
from tasks.schemas import Schema_CelerySchedule

# from .db import Base




class CeleryScheduler(Base):
    __tablename__ = "celery_scheduler"
    pydantic_schema = Schema_CelerySchedule

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    schedule: Mapped[int]  # Интервал в секундах
    task: Mapped[str]
    args: Mapped[str] = mapped_column(nullable=True)
    kwargs: Mapped[str] = mapped_column(nullable=True)

    # task_name = Mapped[str] = mapped_column(index=True)
    # task_args = Mapped[str]
    # task_kwargs = Mapped[str]
    # schedule = Mapped[int]  # Интервал в секундах
    # last_run = Mapped[updated_at]
    

# if __name__ == "__main__":
#     Base.metadata.create_all(bind=sync_engine)