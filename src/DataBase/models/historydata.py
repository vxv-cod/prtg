__all__ = ["Historydata"]

import datetime
from typing import Annotated, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DataBase.db import Base
from DataBase.schemas.historydata import DB_schema_Log_hist_out, DataBase_schema_historydata
from DataBase.dependencies.dep_models import strpk, intpk, created_at, updated_at, datepk
from sqlalchemy import text


# data_format = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))] 


class Historydata(Base):
    __tablename__ = "historydata"
    # pydantic_schema = Prtg_schema_historydata_calculations
    pydantic_schema = DataBase_schema_historydata

    id: Mapped[strpk]
    
    zgd_id: Mapped[int | None] = mapped_column(ForeignKey("zgd.id", ondelete="CASCADE"))
    division_id: Mapped[int | None] = mapped_column(ForeignKey("division.id", ondelete="CASCADE"))
    # division_id: Mapped[int | None]
    date: Mapped[datetime.date]
    pk_name: Mapped[str]
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id", ondelete="CASCADE"))
    type_id: Mapped[int] = mapped_column(ForeignKey("type_sensor.id", ondelete="CASCADE"))

    min_value : Mapped[float]
    avg_value : Mapped[float]
    max_value : Mapped[float]


class LoggingDownload(Base):
    __tablename__ = "logging_download"
    pydantic_schema = DB_schema_Log_hist_out

    id: Mapped[datepk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    count_sensors: Mapped[int]
    status: Mapped[bool]

