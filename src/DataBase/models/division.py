__all__ = ["Management"]

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DataBase.db import Base
from DataBase.dependencies.dep_models import strpk, intpk
from DataBase.schemas.division  import DataBase_schema_division


class Division(Base):
    __tablename__ = "division"
    pydantic_schema = DataBase_schema_division

    id: Mapped[intpk]
    zgd_id: Mapped[int] = mapped_column(ForeignKey("zgd.id", ondelete="CASCADE"))
    name: Mapped[str]
