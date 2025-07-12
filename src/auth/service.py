from .models import User
from .schemas import UserCreate
from .utils import generate_passwd_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        # return False if user is None else True
        return user is not None

    async def user_create(self, user_data: UserCreate, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        
        new_user = User(**user_data)
        
        new_user.password_hash = generate_passwd_hash(user_data_dict['password'])
        
        session.add(new_user)
        
        await session.commit()
        
        return new_user
        
        
        """
        chatgpt style:
        user_data_dict['password_hash'] = generate_password_hash(user_data_dict['password'])

        # Optionally delete plain password
        del user_data_dict['password']

        new_user = User(**user_data_dict)
        """
