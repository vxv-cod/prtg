import io
import json

from docx.document import Document

from docx.opc.part import Part
import docx

from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger

def read_json(file_name):
    '''Из файла json в список Python'''
    with open(file_name, 'r') as fp:
        py_list = json.load(fp)
    return py_list



def write_json(data, file_name):
    '''Запись объектов Python в файл json'''
    with open(f'{file_name}.json', 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)



async def unloading_docx_stream_from_io(filename: str, doc: Document):
    '''Отправляем по стриму налету созданный файл docx'''
    '''Заголовок ответа с указанием способа отображения после загрузки и имени файла'''
    # headers = {'Content-Disposition': f'inline; filename="{filename}"'}
    headers = {'Content-Disposition': f'attachment; filename="{filename}.docx"'}
    '''Создание буфера обмена'''
    buffer = io.BytesIO()
    '''Сохранение документа в буфер обмена'''
    doc.save(buffer)
    buffer.seek(0)

    '''Способ сохранения в темп-файл'''
    # import tempfile
    # with tempfile.NamedTemporaryFile(mode="w+b", suffix=".docx", delete=False) as temp_file:
    #     temp_file.write(buffer.getvalue())
    # # response = FileResponse(temp_file.name, headers=headers)
    
    '''2ой способ выгрузки'''
    # return FileResponse(buffer, headers=headers, media_type="application/docx" )        

    return StreamingResponse(content=buffer, headers=headers, media_type="application/docx")




