import json, datetime
from rich import print as print



def datetime_to_string(string: str, format: str = '%d.%m.%Y %H:%M:%S') -> datetime.datetime:
    ''' Преобразуем dateime в строку 
    format_example = %d.%m.%Y %H:%M:%S '''
    return datetime.datetime.strptime(string, format)


def string_to_datetime(date_time: datetime.datetime, format: str = '%d.%m.%Y %H:%M:%S') -> str:
    ''' Преобразуем строку в dateime
    format_example = %d.%m.%Y %H:%M:%S '''
    return date_time.strftime(format)


def read_data(file: str, type_sensor: str, device: str, block_zgd: str) -> list:
    with open(file, 'r', encoding='utf-8') as file:
        data = []
        histdata = json.load(file)['histdata']
        # print(histdata)

        for row in histdata:
            obj = {}
            list_data_time = row["datetime"].split(' ')
            obj["Устройство"] = device
            obj["Блок ЗГД"] = block_zgd
            obj["Дата"] = list_data_time[0]
            obj["Время"] = ' '.join(list_data_time[1:])
            if type_sensor == "CPU":
                obj["Загрузка CPU, %"] = row["Всего"]
            if type_sensor == "HDD":
                obj["Свободное пространство HDD, %"] = row["Свободное пространство"]
            if type_sensor == "MEMORY":
                obj["Процент доступной памяти MEMORY, МБ"] = row["Процент доступной памяти"]
            data.append(obj)

        return data


def call(file_list: list, device: str, block_zgd: str) -> list:
    '''Объединяем сенсоры в объекты по времени'''
    file_history = []
    count = 0
    for index, file in enumerate(file_list):
        # Для каждого сенсора из списка выбираем нужные поля с данными  
        data = read_data(file=file, type_sensor=sensors[index], device=device, block_zgd=block_zgd)
        # Формируем первоначальный список из объектов с первым сенсором с сортировкой по времени
        if index == 0:
            file_history = [*data]
            count = len(data)
        # Дополняем список из объектов оставшимися сенсорами
        else:
            for idx, value in enumerate(file_history):
                file_history[idx] = {**value, **data[idx]}
            # Проверяем, чтобы все сенсоры имели одинаковую длину списка по предыдущего сенсору
            if count != len(data):
                print(f'''Количество записей сенсора {sensors[index]} не совпадает 
                    с сенсором {sensors[index]}: {count} <> {len(data)}''')
            count = len(data)

    return file_history


def max_and_min(device: str, history: list, block_zgd: str) -> dict:
    '''Группируем данные по дате и времени и приводим, MAX и MIN значения за период'''
    cpu = []; hdd = []; mem = []
    time_start_end_day =[]
    date_grup = []
    date_cpu_hdd_mem = []
    date_pred = ''

    def add_data(i):
        '''Разбиваем данные из списка объектов по разным спискам'''
        cpu.append(i["Загрузка CPU, %"])
        hdd.append(i["Свободное пространство HDD, %"])
        mem.append(i["Процент доступной памяти MEMORY, МБ"])
        ttt = i["Время"].split(" - ")
        eee = [i["Дата"] + " " + s for s in ttt]
        time_start_end_day.append(eee)

    for i in history:
        '''Отслеживаем изменения даты и обнуляем списки'''
        if i["Дата"] != date_pred:
            date_pred = i["Дата"]
            time_start_end_day = []
            cpu = []; hdd = []; mem = []
            '''Наполняем списки данными'''
            add_data(i)
            date_cpu_hdd_mem.append({
                "date" : time_start_end_day,
                "cpu" : cpu, 
                "hdd" : hdd, 
                "mem" : mem
            })
        else:
            add_data(i)
    # print("date_cpu_hdd_mem = ", date_cpu_hdd_mem)

    '''MAX и MIN значения по дням'''
    for i in date_cpu_hdd_mem:
        date_grup.append({
            "Устройство": device,
            "Блок ЗГД": block_zgd,
            "Дата": f'{i["date"][0][0]} - {i["date"][-1][-1]}',
            "cpu": {"max" : max(i["cpu"]), "min" : min(i["cpu"])},
            "hdd": {"max" : max(i["hdd"]), "min" : min(i["hdd"])},
            "mem": {"max" : max(i["mem"]), "min" : min(i["mem"])},
        })
    return date_grup



if __name__ == '__main__':
    file_list = [
        'historicdata_cpu_14999.json', 
        'historicdata_hdd_14993.json', 
        'historicdata_memory_14998.json'
    ]
    sensors = ["CPU", "HDD", "MEMORY"]
    device = "tnnc-czc624b2k4"
    block_zgd = None

    history = call(file_list, device, block_zgd)
    # print("history = ", history)
    # print(json.dumps(file_history, ensure_ascii=False, indent=2))
    date_grup = max_and_min(device, history, block_zgd)
    print(date_grup)




    # obj["date_time_str_start"] = ' '.join(list_data_time[:2])
    # obj["date_time_str_end"] = ' '.join(list_data_time[::3])
    # date_time_obj = datetime.datetime.strptime(' '.join(list_data_time[:2]), '%d.%m.%Y %H:%M:%S')
            

    # Преобразование объектов Python в данные JSON формата, а так же запись в файл 'data.json'
    # with open('data.json', 'w') as fp:
    #     json.dump(file_history, fp, ensure_ascii=False, indent=2)




