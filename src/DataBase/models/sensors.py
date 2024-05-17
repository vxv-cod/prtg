__all__ = ["Sensors", "TypeSensor"]

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DataBase.db import Base
from DataBase.schemas.sensors import DataBase_schema_type_sensor
from prtg.prtg_schema import DataBase_schema_sensor
from DataBase.dependencies.dep_models import intpk



class Sensors(Base):
    __tablename__ = "sensors"
    pydantic_schema = DataBase_schema_sensor

    id: Mapped[intpk]
    type_id: Mapped[int] = mapped_column(ForeignKey("type_sensor.id", ondelete="CASCADE"))
    # sensor: Mapped[str]
    # device: Mapped[str]
    pk_name: Mapped[str]

    type_sensor: Mapped["TypeSensor"] = relationship(back_populates="sensors")



class TypeSensor(Base):
    __tablename__ = "type_sensor"
    pydantic_schema = DataBase_schema_type_sensor

    id: Mapped[intpk]
    type: Mapped[str]
    value: Mapped[str]

    sensors: Mapped[list["Sensors"]] = relationship(back_populates="type_sensor")

