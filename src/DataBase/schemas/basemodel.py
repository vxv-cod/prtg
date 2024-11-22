import datetime
from pydantic import BaseModel



class Base_Model(BaseModel):
    id : int | str
    class Config:
        from_attributes = True 
