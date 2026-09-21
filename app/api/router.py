from fastapi import APIRouter
from app.api.v1.api import api_router as v1_router

base_router = APIRouter()

base_router.include_router(v1_router, prefix="/v1")