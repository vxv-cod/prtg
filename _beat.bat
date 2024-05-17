CALL venv\Scripts\activate.bat
wt --title celery_beet py src\celery_run_beet.py

@REM cd src
@REM wt --title celery_beet py celery_run_beet.py
@REM wt --title celery_beet celery -A src.celery_app:celery_app beat -S sqlalchemy_celery_beat.schedulers:DatabaseScheduler -l info 