import uvicorn
from fastapi import FastAPI


application = FastAPI()


@application.get("/ping")
def pong():
    return "pong"


def start():
    uvicorn.run("mbb.main:application", host="0.0.0.0", port=8008, reload=True)
