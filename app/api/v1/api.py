from fastapi import APIRouter
from app.api.v1.endpoints.check import router as check_router
from app.api.v1.endpoints.usuario import router as users_router
from app.api.v1.endpoints.admin import router as admins_router
from app.api.v1.endpoints.alimentador import router as alimentadores_router

api_router = APIRouter()

api_router.include_router(check_router, prefix="/check", tags=["Check"])
api_router.include_router(users_router, prefix="/usuarios", tags=["Users"])
api_router.include_router(admins_router, prefix="/admins", tags=["Admins"])
api_router.include_router(alimentadores_router, prefix="/alimentadores", tags=["Alimentadores"])