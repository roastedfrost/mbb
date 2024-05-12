import uvicorn
from fastapi import FastAPI
from mbb.moex.router import router as moex_router
from mbb.settings import settings


application = FastAPI()


application.include_router(moex_router, prefix="/moex")


@application.get("/ping")
def pong():
    return "pong"


def start():
    print(settings.model_dump())
    uvicorn.run("mbb.main:application", host="0.0.0.0", port=8008, reload=True)
