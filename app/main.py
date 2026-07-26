
from fastapi import FastAPI

from app.routers import philosophers, quotes

app = FastAPI(
    title="a python api to get famous philosophers quotes"
)

app.include_router(philosophers.router)
app.include_router(quotes.router)


@app.get("/")
async def ping():
    return {"ping": "pong"}
