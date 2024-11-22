@ECHO off 
@REM chcp 866
@REM CALL SET https_proxy=http://tmn-tnnc-proxy.rosneft.ru:9090
IF EXIST "%cd%\venv" (
	CALL venv\Scripts\activate.bat
	CALL py -V
	ECHO Виртуальное окружение активировано в папке : %cd%
	CALL pip list
) ELSE (echo Папка с именем "venv" не найдена)
CMD 
