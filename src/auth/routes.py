from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta

from .schemas import UserCreate, User, UserLogin
from .service import UserService
from .utils import create_access_token, decode_token, verify_password
from src.db.main import get_session

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post(
    "/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
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
    new_user = await user_service.user_create(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_users(
    login_data: UserLogin, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password"
        )
        
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password"
        )
        
    access_token = create_access_token(
                user_data={"email": user.email, "user uid": str(user.uid)}
            )
    refresh_token = create_access_token(
        user_data={"email": user.email, "user uid": str(user.uid)},
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
        refresh=True
    )
            
    return JSONResponse(
        content={
            "message": "Login Successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "uid": str(user.uid)
            }
        }
    )

    # if user is not None:
    #     is_password_valid = verify_password(password, user.password_hash)

    #     if is_password_valid:
    #         access_token = create_access_token(
    #             user_data={"email": user.email, "user uid": str(user.uid)}
    #         )
    #         refresh_token = create_access_token(
    #             user_data={"email": user.email, "user uid": str(user.uid)},
    #             expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
    #             refresh=True
    #         )
            
    #         return JSONResponse(
    #             content={
    #                 "message": "Login Successful",
    #                 "access_token": access_token,
    #                 "refresh_token": refresh_token,
    #                 "user": {
    #                     "email": user.email,
    #                     "uid": str(user.uid)
    #                 }
    #             }
    #         )
            