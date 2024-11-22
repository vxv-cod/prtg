__all__ = ["Zgd"]

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DataBase.db import Base
from DataBase.dependencies.dep_models import strpk, intpk
from DataBase.schemas.zgd  import DataBase_schema_zgd


class Zgd(Base):
    __tablename__ = "zgd"
    pydantic_schema = DataBase_schema_zgd

    id: Mapped[intpk]
    name: Mapped[str]
