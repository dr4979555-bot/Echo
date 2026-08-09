from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from database.database import engine, Base
from database import models

from api.health import router as health_router
from api.init import router as init_router
from api.feed import router as feed_router
from api.run import router as run_router

from api.memory import router as memory_router

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The Autonomous AI Technology Explorer",
    version=settings.VERSION
)


# ==============================
# CORS Configuration
# ==============================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        "http://localhost:5174",
        "http://127.0.0.1:5174",

        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# API Routers
# ==============================

app.include_router(health_router)
app.include_router(init_router)
app.include_router(feed_router)
app.include_router(run_router)
app.include_router(memory_router)

# ==============================
# Root Endpoint
# ==============================

@app.get("/")
def home():
    return {
        "project": settings.PROJECT_NAME,
        "message": "Autonomous AI Technology Explorer is running 🚀"
    }