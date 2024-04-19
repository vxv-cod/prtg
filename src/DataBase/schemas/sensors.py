from .basemodel import Base_Model



class DataBase_schema_type_sensor(Base_Model):
    id: int
    type: str
    value: str


class DataBase_schema_sensor(Base_Model):
    id: int
    type_id: int
    pk_name: str


# class DataBase_schema_sensor_in(Base_Model):
#     sensor: str
#     type: str
#     device: str
#     pk_name: str
    


