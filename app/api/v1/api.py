from fastapi import APIRouter
from app.api.v1.endpoints.check import router as check_router
from app.api.v1.endpoints.usuario import router as users_router

api_router = APIRouter()

api_router.include_router(check_router, prefix="/check", tags=["Check"])
api_router.include_router(users_router, prefix="/usuarios", tags=["Users"])