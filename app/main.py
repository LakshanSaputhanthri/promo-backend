from fastapi import FastAPI
from app.routers import promotions

app = FastAPI(title="Promotions API", version="0.1.0")

app.include_router(promotions.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
