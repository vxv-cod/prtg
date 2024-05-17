from tasks.celery_app import celery_app


worker = [
    "worker", 
    "--pool=threads", 
    "--loglevel=info", 
    "broker_connection_retry_on_startup=True"
]
print(f"Запуск celery: {' '.join(worker)} \n")


if __name__ == "__main__":
    celery_app.start(worker)


# gevent работает также как и threads потоками, на при запуске через этот файл пропадает процесс
# loglevel: DEBUG INFO WARNING ERROR CRITICAL FATAL