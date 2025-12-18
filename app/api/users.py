from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.session import get_db
from app.db.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.utils.jwt import JWTHandler
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=list[UserRead])
async def list_users(
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    return await repo.list()

@router.get("/me", response_model=UserRead)
async def me(
    current_user: Annotated[User, Depends(JWTHandler().verify_token)],
):
    return current_user