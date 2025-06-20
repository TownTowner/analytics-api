from typing import Union

from fastapi import FastAPI
from api.events import eventRT
from api.db.session import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # 关闭数据库连接
    # session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(eventRT, prefix="/api/events")

# docker: python:3.6.15-slim-buster


@app.get("/")
async def read_root():
    return {"Hello": "Worlder"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/healthz")
async def read_api_health():
    return {"status": "OK"}
