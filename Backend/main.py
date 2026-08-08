from fastapi import FastAPI

from core.config import settings

from database.database import engine, Base
from database import models

from api.health import router as health_router
from api.init import router as init_router
from api.feed import router as feed_router
from api.run import router as run_router


# Create database tables

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The Autonomous AI Technology Explorer",
    version=settings.VERSION
)


# API Routers

app.include_router(health_router)
app.include_router(init_router)
app.include_router(feed_router)
app.include_router(run_router)


@app.get("/")
def home():

    return {
        "project": settings.PROJECT_NAME,
        "message": "Autonomous AI Technology Explorer is running 🚀"
    }