import sys
import uvicorn
from fastapi import FastAPI
# from rich import print
from fastapi.middleware.cors import CORSMiddleware
from a2wsgi import ASGIMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from main_routers import all_routers

# from create_celery import celery_app
# from tasks.custom_scheduler import CustomScheduler
# celery_app.conf.beat_scheduler = CustomScheduler

# sys.path.append("..")

app = FastAPI(
    title="Prtg API"
)


origins = [
    "http://localhost:8888",
    "http://localhost:8000",
    "http://localhost:443/",
    "http://127.0.0.1:5000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin", "Authorization"],
)


for router in all_routers:
    app.include_router(router)



# @app.on_event("startup")
# async def startup():
#     # redis = aioredis.from_url("redis://localhost")
#     redis = aioredis.from_url("redis://localhost:6379")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")



wsgi_app = ASGIMiddleware(app)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="127.0.0.1", port=5500)
    # sys.exit(wsgi_app)

    