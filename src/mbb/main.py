import uvicorn
from fastapi import FastAPI
from mbb.moex.router import router as moex_router
from mbb.settings import settings


application = FastAPI()


application.include_router(moex_router, prefix="/moex")


def start():
    uvicorn.run("mbb.main:application", host=settings.host, port=settings.port, reload=True)
