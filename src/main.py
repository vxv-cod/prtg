import sys
import uvicorn
from fastapi import FastAPI
# from rich import print
from fastapi.middleware.cors import CORSMiddleware
from a2wsgi import ASGIMiddleware


from main_routers import all_routers



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


wsgi_app = ASGIMiddleware(app)


if __name__ == "__main__":
    # uvicorn.run(app="main:app", reload=True)
    # sys.exit(wsgi_app)
    uvicorn.run(
        app="main:app",
        reload=True,
        host="127.0.0.1",
        port=5500
    )
    