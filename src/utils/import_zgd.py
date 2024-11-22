import os
import shutil
import sys
from fastapi import UploadFile
from loguru import logger
from openpyxl import load_workbook
from rich import print


if __name__ == "__main__":
    sys.path.insert(1, os.path.join(sys.path[0], '..'))



def save_file(file: UploadFile):
    with open('src/store/' + file.filename, "wb") as wf:
        # wf.write(file.file.read())
        shutil.copyfileobj(file.file, wf)
        file.file.close() # удалаяет временный
        


def set_user_zgd(filename: str = 'src/store/ZGD.xlsx', sheet: str = 'Свод', fist_row: int = 2):
    '''Загружаем из файла id компа, его блок ЗГД и описание блока'''
    def obj_dict(row):
        return {"id": row[1], "block_zgd": row[2], "description": row[3]}
    '''Загружаем из файла объект екселя'''
    wb = load_workbook(filename = filename)
    '''Выбираем из всех данных листа по строчкно нужные поля'''
    rows = [obj_dict(row) for row in wb[sheet].values]
    '''Пересобираем список без первой строки с названием колонок'''
    rows = rows[fist_row - 1 : ]
    '''Преобразуем строки в словарь с ключами по id для перезапись одинаковых строк'''
    unic_dict = {row["id"] : row for row in rows}
    '''Возаращаем уникальные строки'''
    unic_rows = list(unic_dict.values())
    '''Сохраняем в файл в store'''
    wb.save("src/store/ZGD.xlsx")
    '''Закрываем wb'''
    wb.close()
    print("Данные получены")
    return unic_rows



def set_zgd():
    def obj_dicttt(idx, row):
        return {"id": idx, "name": row}
    unic_rows = set_user_zgd()
    '''Убираем одинаковые Управления из списка'''
    zgd_set: set = sorted(list(set([v["block_zgd"] for v in unic_rows])))
    '''Собираем словари с id управления и блоком ЗГД'''
    zgd_list = [obj_dicttt(idx, row) for idx, row in enumerate(zgd_set)]
    print(zgd_list)
    return zgd_list


def set_division():
    def zgd_id_set(block_zgd):
        for i in zgd:
            if block_zgd == i["name"]:
                return i["id"]
    def obj_dicttt(idx, row):
        return {"id": idx, "name": row[0], "zgd_id": zgd_id_set(row[1])}
    unic_rows = set_user_zgd()
    zgd = set_zgd()

    '''Убираем одинаковые Управления из списка'''
    div_dict: dict = {v["description"]: v["block_zgd"] for i, v in enumerate(unic_rows)}
    '''Собираем словари с id управления и блоком ЗГД'''
    div_list = [obj_dicttt(idx, row) for idx, row in enumerate(div_dict.items())]
    print(div_list[-1])
    return div_list



def drop_tables():
    from DataBase.db import sync_engine, Base
    # from DataBase.models import (sensors,historydata,user_zgd,division,zgd)
    from DataBase import models

    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)

    
if __name__ == "__main__":
    from rich import print
    drop_tables()
    unic_rows = set_user_zgd()
    set_division()
    set_zgd()
    ...
    