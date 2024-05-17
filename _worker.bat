CALL venv\Scripts\activate.bat
wt --title celery_worker py src\celery_run_worker.py

@REM wt --title celery_worker celery -A src.celery_app:celery_app worker -P gevent -l info broker_connection_retry_on_startup=True
@REM wt --title celery_worker celery -A src.celery_app:celery_app worker -P threads -l info broker_connection_retry_on_startup=True
