from fastapi import APIRouter
from .schemas import UserCreate

auth_router = APIRouter()

@auth_router.post('/signup')
async def create_user_account(user_data: UserCreate):
    pass