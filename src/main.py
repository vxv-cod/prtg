import os

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



from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    # get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Prtg API",
	docs_url=None, 
	redoc_url=None
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

'''Для того чтоб файлы стали доступны для скачивания нужно добавить ссылку'''
# app.mount('/download', StaticFiles(directory="src/store"), name="download")
# http://127.0.0.1:5500/download/ZGD.xlsx



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.ico",
    )


# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )



# origins = [
#     "http://localhost:8888",
#     "http://localhost:5500",
#     "http://localhost:443/",
#     "http://127.0.0.1:5000/",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
#     allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
#                    "Access-Control-Allow-Origin", "Authorization"],
# )


for router in all_routers:
    app.include_router(router)



# @app.on_event("startup")
# async def startup():
    # redis = aioredis.from_url("redis://localhost")
    # redis = aioredis.from_url("redis://localhost:6379")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")



wsgi_app = ASGIMiddleware(app)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="127.0.0.1", port=5500)


    # sys.exit(wsgi_app)

    