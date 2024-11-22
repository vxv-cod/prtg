import datetime
from DataBase.repositories.repo_api import (
    Api_DB_division,
    Api_DB_files,
    Api_DB_sensors,
    Api_DB_historydata, 
    Api_DB_type_sensor, 
    Api_DB_user_zgd,
    Api_DB_logging,
    Api_DB_zgd
)
from DataBase.schemas.division import DataBase_schema_division
from DataBase.schemas.historydata import DB_schema_Log_hist_out, DB_schema_Log_hist_in, DataBase_schema_historydata
from DataBase.schemas.sensors import DataBase_schema_sensor, DataBase_schema_type_sensor
from DataBase.schemas.user_zgd import DataBase_schema_user_zgd
from DataBase.schemas.zgd import DataBase_schema_zgd
from utils.functions import read_json



api_obj_sensors = Api_DB_sensors(
    prefix = "/DataBase/sensors", 
    tags = ["DataBase: sensors"], 
    attr_uow_name = "sensors",
    db_shama_in = DataBase_schema_sensor,
    db_shama_out = DataBase_schema_sensor,
    typeid = int,
)


# api_obj_historydata = Api_DB_default(
api_obj_historydata = Api_DB_historydata(
    prefix = "/DataBase/historydata", 
    tags = ["DataBase: historydata"], 
    attr_uow_name = "historydata",
    db_shama_in = DataBase_schema_historydata,
    db_shama_out = DataBase_schema_historydata,
    typeid = str,
    )



api_type_sensor = Api_DB_type_sensor(
    prefix = "/DataBase/type_sensor", 
    tags = ["DataBase: type_sensor"], 
    attr_uow_name = "type_sensor",
    db_shama_in = DataBase_schema_type_sensor,
    db_shama_out = DataBase_schema_type_sensor,
    typeid = int,
)
api_type_sensor.default_data = read_json("src\store\default_data.json")["default_type_sensor"]
# api_type_sensor.default_data = read_json("store\default_data.json")["default_type_sensor"]


api_logging_download = Api_DB_logging(
    prefix = "/prtg", 
    tags = ["DataBase: logging"], 
    attr_uow_name = "logging_download",
    db_shama_in = DB_schema_Log_hist_in,
    db_shama_out = DB_schema_Log_hist_out,
    typeid = datetime.date,
)



api_user_zgd = Api_DB_user_zgd(
    prefix = "/DataBase/user_zgd", 
    tags = ["DataBase: user_zgd"], 
    attr_uow_name = "user_zgd",
    db_shama_in = DataBase_schema_user_zgd,
    db_shama_out = DataBase_schema_user_zgd,
    typeid = str,
)


api_division = Api_DB_division(
    prefix = "/DataBase/division", 
    tags = ["DataBase: division"], 
    attr_uow_name = "division",
    db_shama_in = DataBase_schema_division,
    db_shama_out = DataBase_schema_division,
    typeid = int,
)



api_zgd = Api_DB_zgd(
    prefix = "/DataBase/zgd", 
    tags = ["DataBase: zgd"], 
    attr_uow_name = "zgd",
    db_shama_in = DataBase_schema_zgd,
    db_shama_out = DataBase_schema_zgd,
    typeid = int,
)


api_files = Api_DB_files(
    prefix = "/files", 
    tags = ["files"], 
)

