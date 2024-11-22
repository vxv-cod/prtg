CALL venv\Scripts\activate.bat
@REM wt --title celery_worker py src\celery_run_worker.py

CALL cd src
wt --title celery_worker celery -A tasks.celery_app:celery_app worker -P solo -l INFO broker_connection_retry_on_startup=True
@REM wt --title celery_worker celery -A tasks.celery_app:celery_app worker -P threads -l WARNING broker_connection_retry_on_startup=True
@REM gevent solo
@REM loglevel: DEBUG INFO WARNING ERROR CRITICAL FATAL
