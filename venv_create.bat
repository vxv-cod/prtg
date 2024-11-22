@ECHO off 
chcp 65001
IF NOT EXIST "%APPDATA%\pip\pip.ini" (
	@REM call pip config set global.trusted-host "pypi.python.org pypi.org files.pythonhosted.org"
	@REM call pip config set global.user false
	@REM @REM global.proxy нужна для работы pip (проверенная версия от 24.1.1)
	@REM call pip config set global.proxy %content%

	call pip config set global.disable-pip-version-check True
	call pip config set global.index "https://nexus-tnnc/repository/python"
	call pip config set global.index-url "https://nexus-tnnc/repository/python/simple"
	call pip config set global.timeout 240
	call pip config set global.trusted-host "nexus-tnnc"
)

IF NOT EXIST "%cd%\venv" (
	ECHO Создается виртуального окрружения: "%cd%\venv" ... 
	@REM CALL python -m venv venv
	CALL py -m venv venv
)
ECHO Активируем venv ...
CALL venv\Scripts\activate.bat 
ECHO Виртуальное окружение активировано: "%cd%\venv" ...

ECHO Обновление модуля pip ...
CALL venv\Scripts\python.exe -m pip install --upgrade pip

ECHO Обновление модуля setuptools ...
CALL venv\Scripts\python.exe -m pip install --upgrade setuptools

ECHO Текущее состояние пакетов ...
CALL pip list

@REM Устанавка пакетв из файла requirements.txt
IF EXIST "%cd%\dev_requirements.txt" (
	ECHO Установка пакетов из файла dev_requirements.txt ...
	CALL pip install -r dev_requirements.txt
	CALL pip list
	ECHO Установка пакетов из файла dev_requirements.txt завершена.
) ELSE (
	ECHO Для установки пакетов в виртуальное окружение создайте файл dev_requirements.txt в текущей папке, с указанием названий нужных пакетов ...
	ECHO Для ручной установки пропишите команду: pip install Имя_пакета
)

cmd