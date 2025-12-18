from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.session import get_db
from app.db.repositories.otp import OTPRepository
from app.db.repositories.user import UserRepository
from app.schemas.otp import OTPCreate, OTPRead, OTPVerify, OTPUpdate
from app.schemas.user import UserCreate
from app.schemas.jwt import JWTToken
from app.utils.exceptions import NotFoundException
from app.utils.jwt import JWTHandler

router = APIRouter()


@router.post("/otp-send", response_model=OTPRead, status_code=status.HTTP_200_OK)
async def send(
    data: Annotated[OTPCreate, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user_repo = UserRepository(db)
    try:
        user_record = await user_repo.get_by_unique_fields(**{data.field: data.address})
    except NotFoundException:
        user_record = await user_repo.create(UserCreate(**data.model_dump()))
    otp_repo = OTPRepository(db)
    return await otp_repo.create(user=user_record, data=data)


@router.post("/otp-verify", response_model=JWTToken, status_code=status.HTTP_200_OK)
async def verify(
    data: Annotated[OTPVerify, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user_repo = UserRepository(db)
    user_record = await user_repo.get_by_unique_fields(**{data.field: data.address})

    otp_repo = OTPRepository(db)
    otp_record = await otp_repo.get_for_verify(
        code=data.otp, field=data.field, address=data.address
    )
    otp_record = await otp_repo.update(otp_record, OTPUpdate(used=True))

    return JWTHandler().generate_token(user=user_record)
    # return data.model_dump()
