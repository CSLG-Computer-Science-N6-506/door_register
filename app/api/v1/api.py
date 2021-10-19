from app import api
from fastapi import APIRouter

from app.api.v1.views import raspi, user,login,member

api_router = APIRouter()

api_router.include_router(login.router, tags=['login'])
api_router.include_router(user.router, tags=['user'], prefix='/auth')
api_router.include_router(member.router,tags=['lab'])
api_router.include_router(raspi.router,prefix='/register',tags=['raspi'])