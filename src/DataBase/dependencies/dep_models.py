import datetime
from typing import Annotated


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text


'''Поля DataBase'''
intpk = Annotated[int, mapped_column(primary_key=True)]
strpk = Annotated[str, mapped_column(primary_key=True)]
# datepk = Annotated[datetime.date, mapped_column(primary_key=True)]
# created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
# updated_at = Annotated[datetime.datetime, mapped_column(
#         server_default=text("TIMEZONE('utc', now())"),
#         onupdate=datetime.datetime.utcnow,
#     )]

datepk = Annotated[datetime.date, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text('now()')
)]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text('now()'),
    onupdate=datetime.datetime.now,
)]



