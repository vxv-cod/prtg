@ECHO off 
chcp 65001

call cd %cd%
CALL venv\Scripts\activate.bat
ECHO Виртуальное окружение активировано в папке : %cd%

wt --title redis-server %cd%\Redis-x64-5.0.14.1\redis-server.exe; ^
sp -V -s 0.3 --title redis-cli %cd%\Redis-x64-5.0.14.1\redis-cli.exe; ^
nt --title celery_worker py src\celery_run_worker.py; ^
sp -V -s .5 --title celery_beet py src\celery_run_beet.py; ^
sp -H -s .33 --title celery_flower py src\celery_run_flower.py; ^
nt --title main py src\main.py