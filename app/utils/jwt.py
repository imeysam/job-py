from fastapi import Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Annotated
import jwt
from zoneinfo import ZoneInfo

from app.db.session import get_db
from app.utils.exceptions import UnauthorizedException, ForbiddenException
from app.schemas.jwt import JWTToken
from app.db.models import User
from app.core.config import settings
from app.db.repositories.user import UserRepository


class JWTHandler:

    def __init__(self) -> None:
        self.timezone = ZoneInfo(settings.TIME_ZONE)
        self.now = datetime.now(tz=self.timezone)
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.expire = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    def generate_token(self, user: User, exp_minutes: int | None = None) -> JWTToken:
        exp_minutes = exp_minutes if exp_minutes is not None else self.expire

        payload = {
            "data": user.id,
            "exp": self.now + timedelta(minutes=exp_minutes),
        }

        encoded_jwt = jwt.encode(payload, self.secret_key, self.algorithm)
        return JWTToken(access=encoded_jwt, exp=int(payload["exp"].timestamp()))

    async def verify_token(
        self,
        jwt_token: Annotated[str, Header()],
        db: Annotated[AsyncSession, Depends(get_db)],
    ) -> User:
        try:
            token_data = jwt.decode(
                jwt_token, self.secret_key, algorithms=[self.algorithm]
            )
            if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
                raise UnauthorizedException(detail="Token expired")
        except jwt.exceptions.PyJWTError:
            raise ForbiddenException(detail="Could not validate credentials.")

        return await UserRepository(db).get_by_unique_fields(id=token_data["data"])
