from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.db_connection import db_manager
from app.core.config import settings
from app.api.router import base_router
from mangum import Mangum

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.initialize()
    yield
    await db_manager.close()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(base_router)

handler: Mangum = Mangum(app=app)