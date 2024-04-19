from loguru import logger
from openpyxl import load_workbook
from rich import print



def load_zgd(filename: str = 'src/store/ZGD.xlsx', sheet: str = 'Свод', fist_row: int = 2):
    # logger.error(f"{filename = }")
    '''Загружаем из файла id компа, его блок ЗГД и описание блока'''

    def obj_dict(row):
        return {"id": row[1], "block_zgd": row[2], "description": row[3]}

    wb = load_workbook(filename = filename)
    # wb = load_workbook(filename = filename + ".xlsx")
    rows = [obj_dict(row) for row in wb[sheet].values]
    rows = rows[fist_row - 1 : ]
    wb.close()
    # wb.save("aaaaaaa.xlsx")
    print("Данные получены")
    return rows



if __name__ == "__main__":
    from rich import print
    result = load_zgd()
    print(result)
