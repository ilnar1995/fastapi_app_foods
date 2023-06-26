import asyncio
from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import Response
#from core.db import SessionLocal
from src.core.db import async_session_maker

from src.routes import routes


app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):   #для создания сессии при каждом запросе в api
    response = Response("Internal server error", status_code=500)
    try:
        # request.state.db = SessionLocal()  # для синхрон запросов
        request.state.db = async_session_maker()  # для асинхрон запросов
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


app.include_router(routes)

