@REM wt %cd%\start_redis.bat & 
@REM wt %cd%\start_celery.bat &
@REM wt %cd%\start_flower.bat
@REM CMD


@REM CALL  %cd%\venv\Scripts\activate.bat &
@REM wt nt --title redis-server %cd%\Redis-x64-5.0.14.1\redis-server.exe; sp --title redis-cli %cd%\Redis-x64-5.0.14.1\redis-cli.exe
@REM wt nt --title celery-worker -d %cd%\src celery -A tasks.create_celery:celery_app worker --loglevel=INFO --pool=solo broker_connection_retry_on_startup=True; sp --title celery-flower -d %cd%\src celery -A tasks.create_celery:celery_app flower --port=5555


@REM CALL  %cd%\venv\Scripts\activate.bat &
@REM wt nt --title redis-server %cd%\Redis-x64-5.0.14.1\redis-server.exe
@REM wt nt --title celery-worker -d %cd%\src celery -A tasks.create_celery:celery_app worker --loglevel=INFO --pool=solo broker_connection_retry_on_startup=True
@REM wt nt --title celery-flower -d %cd%\src celery -A tasks.create_celery:celery_app flower --port=5555


@REM DEBUG INFO WARNING ERROR CRITICAL FATAL
CALL  %cd%\venv\Scripts\activate.bat
wt --title redis-server %cd%\Redis-x64-5.0.14.1\redis-server.exe; sp --title redis-cli %cd%\Redis-x64-5.0.14.1\redis-cli.exe
wt nt --title celery-worker -d %cd%\src celery -A tasks.create_celery:celery_app worker -P gevent -l WARNING broker_connection_retry_on_startup=True
wt nt --title celery-flower -d %cd%\src celery -A tasks.create_celery:celery_app flower --port=5555


@REM (
@REM     wt --title redis-server %cd%\Redis-x64-5.0.14.1\redis-server.exe; 
@REM     sp --title redis-cli %cd%\Redis-x64-5.0.14.1\redis-cli.exe; 
@REM     nt --title celery-worker -d %cd%\src celery -A tasks.create_celery:celery_app worker -P gevent -l WARNING broker_connection_retry_on_startup=True; 
@REM     nt --title celery-flower -d %cd%\src celery -A tasks.create_celery:celery_app flower --port=5555
@REM )
