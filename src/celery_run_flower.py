from tasks.celery_app import celery_app
from config import settings



worker = [
    "flower", 
    f"--port={settings.FLOWER_PORT}", 
    "--loglevel=info"
]
print(f"Запуск celery: {' '.join(worker)} \n")



if __name__ == "__main__":
    celery_app.start(worker)
