from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.scheduler import start_scheduler
from app.routers import promotions


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(promotions.router)
