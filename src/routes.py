from fastapi import APIRouter
from src.menu import router as menu_router


routes = APIRouter()


routes.include_router(
    menu_router.router,
    prefix="/menu",
    tags=["Menu"],
)



