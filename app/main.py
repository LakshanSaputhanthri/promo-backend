from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.scheduler import start_scheduler
from app.routers import promotions
from app.features.hnb import refresh_hnb_promotions
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await refresh_hnb_promotions()
    start_scheduler()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] to allow all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods GET, POST, etc.
    allow_headers=["*"],  # allow all headers
)


app.include_router(promotions.router)
