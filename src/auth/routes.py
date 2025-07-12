from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import UserCreate
from .service import UserService
from src.db.main import get_session

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup")
async def create_user_account(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists",
        )
    new_user = await user_service.user_create(user_data)
    
    return new_user