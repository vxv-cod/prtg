from loguru import logger

from alembic.config import Config
from alembic import command


def migrate_downgrade_base(alembic_cfg):
    command.downgrade(alembic_cfg, "base")
    logger.debug("Тублицы из ДБ удалены ...")


def create_migrate_revision(alembic_cfg, name_revision: str):
    command.revision(config=alembic_cfg, message=f"{name_revision}", autogenerate=True)
    logger.debug("Ревизия миграции создана ...")


def migrate_upgrade(alembic_cfg):
    command.upgrade(alembic_cfg, "head")
    logger.debug("Миграция выполнена ...")


def migrate_downgrade(alembic_cfg):
    command.downgrade(alembic_cfg, '-1')
    logger.debug("Миграция выполнена ...")



if __name__ == "__main__":
    # name_revision = input("Введите има ревизии миграции: ",)
    alembic_cfg = Config("alembic.ini")
    name_revision = "Creat_table"
    # name_revision = "correct_table_1"
    
    # migrate_downgrade_base(alembic_cfg)
    # migrate_downgrade(alembic_cfg)
    
    # create_migrate_revision(alembic_cfg, name_revision)
    migrate_upgrade(alembic_cfg)






