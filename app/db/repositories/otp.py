from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.otp import OTP
from app.db.models.user import User
from app.schemas.otp import OTPCreate, OTPRead, OTPUpdate
from random import randint
from datetime import datetime, timedelta
from app.utils.exceptions import NotFoundException


class OTPRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User, data: OTPCreate) -> OTPRead:
        record = OTP(
            user_id=user.id,
            field_name=data.field,
            field_address=data.address,
            code=randint(111111, 999999),
            expired_at=str(datetime.now() + timedelta(minutes=10)),
        )
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def get_for_verify(self, code: int, field: str, address: str) -> OTP:
        query = (
            select(OTP)
            .where(OTP.code == code)
            .where(OTP.field_name == field)
            .where(OTP.field_address == address)
            .where(OTP.used == False)
            .where(OTP.expired_at > datetime.now())
        )
        result = await self.session.execute(query)
        result = result.scalars().first()
        if not result:
            raise NotFoundException(detail="OTP Not Found")
        return result

    async def update(self, record: OTP, data: OTPUpdate) -> OTP:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(record, field, value)

        await self.session.commit()
        await self.session.refresh(record)
        return record
    
    async def list(self) -> list[OTP]:
        result = await self.session.execute(select(OTP))
        return result.scalars().all()
