from tasks.celery_app import celery_app
from sqlalchemy_celery_beat.schedulers import DatabaseScheduler


worker = [
    "beat",
    "--loglevel=info"
    # "--loglevel=debug"
]
print(f"Запуск celery: {' '.join(worker)} \n")

if __name__ == "__main__":
    celery_app.start(worker)
    # celery_app.start(["beat","--loglevel=info"])