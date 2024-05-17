from tasks.celery_app import celery_app
from sqlalchemy_celery_beat.schedulers import DatabaseScheduler


worker = [
    "beat",
    # "--scheduler=sqlalchemy_celery_beat.schedulers:DatabaseScheduler",
    "--loglevel=info"
]
print(f"Запуск celery: {' '.join(worker)} \n")

if __name__ == "__main__":
    celery_app.start(worker)