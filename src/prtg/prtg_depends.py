from typing import Annotated

from fastapi import Depends

from prtg.prtg_schema import Prtg_schema_historydata_input, Prtg_schema_Sensor
from prtg.prtg_uow import Prtg_UOW



'''Prtg'''
Prtg_depend_UOW = Annotated[Prtg_UOW, Depends()]
Prtg_depend_historydata_input = Annotated[Prtg_schema_historydata_input, Depends()]
Prtg_depend_Prtg_schema_Sensor = Annotated[Prtg_schema_Sensor, Depends()]





