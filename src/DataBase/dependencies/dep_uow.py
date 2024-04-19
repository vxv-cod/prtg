from typing import Annotated
from fastapi import Depends
from DataBase.repositories.repo_uow import UnitOfWork


'''DataBase'''
DataBase_depend_UOW = Annotated[UnitOfWork, Depends()]






