from DataBase.models.division import Division
from DataBase.models.user_zgd import User_zgd
from DataBase.models.zgd import Zgd
from DataBase.repositories.repo_SQLAlchemy import SQLAlchemyRepository
from DataBase.models.sensors import Sensors, TypeSensor
from DataBase.models.historydata import Historydata, LoggingDownload



class SensorsRepository(SQLAlchemyRepository):
    model = Sensors


class HistorydataRepository(SQLAlchemyRepository):
    model = Historydata


class TypeSensorRepository(SQLAlchemyRepository):
    model = TypeSensor


class LoggingDownloadRepository(SQLAlchemyRepository):
    model = LoggingDownload
    
class UserRepository(SQLAlchemyRepository):
    model = User_zgd
    
    
class DivisionRepository(SQLAlchemyRepository):
    model = Division
    
    
class ZgdRepository(SQLAlchemyRepository):
    model = Zgd
    
