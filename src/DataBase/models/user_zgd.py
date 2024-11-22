__all__ = ["User_zgd"]

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DataBase.db import Base
# from .dep import intpk
from DataBase.dependencies.dep_models import strpk
from DataBase.schemas.user_zgd import DataBase_schema_user_zgd



class User_zgd(Base):
    __tablename__ = "user_zgd"
    pydantic_schema = DataBase_schema_user_zgd

    id: Mapped[strpk]
    block_zgd: Mapped[str]
    description: Mapped[str]
