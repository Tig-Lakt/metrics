import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.endpoints import message, process
from app.api import health
from seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()
    # Подключения к БД
    yield   


app = FastAPI(title="FastAPI Observability",
    lifespan=lifespan)

app.include_router(health.router)
app.include_router(message.router, tags=["Message"])
app.include_router(process.router, tags=["Process"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)