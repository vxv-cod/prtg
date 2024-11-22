from enum import StrEnum
from loguru import logger

# from tasks.tasks_repo import TasksRepository



# EnumTasks_task = StrEnum(
#     value="EnumTasks_task",
#     names=(TasksRepository.get_all_task_name()),
# )



'''Вариант с хардкодом'''
from enum import Enum, StrEnum

# class EnumTasks_task(StrEnum):
class EnumTasks_task(str, Enum):
    auto_import_histor = "tasks.tasks_repo.auto_import_histor"
    add_test_task = "tasks.tasks_repo.import_sensors_in_DB"


