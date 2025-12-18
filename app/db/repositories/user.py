from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.utils.exceptions import NotFoundException

class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate) -> User:
        payload = {
            data.field: data.address
        }
        user = User(**payload)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    # async def create(self, data: UserCreate) -> User:
    #     user = User(**data.model_dump())
    #     self.session.add(user)
    #     await self.session.commit()
    #     await self.session.refresh(user)
    #     return user

    async def get_by_unique_fields(self, **kwargs) -> User:
        query = select(User)
        
        for key, value in kwargs.items():
            if hasattr(User, key):
                query = query.where(getattr(User, key) == value)
        result = await self.session.execute(query)
        result = result.scalars().first()
        if not result:
            raise NotFoundException(error="User Not Found")
        return result
    
    async def list(self) -> list[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()
