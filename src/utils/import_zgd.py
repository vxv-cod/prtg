from loguru import logger
from openpyxl import load_workbook
from rich import print



def load_zgd(filename: str = 'src/store/ZGD.xlsx', sheet: str = 'Свод', fist_row: int = 2):
    logger.error(f"{filename = }")
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



# if __name__ == "__main__":
#     from rich import print
#     result = load_zgd()
#     print(f"{result = }")
