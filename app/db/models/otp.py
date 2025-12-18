from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.types import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

class OTP(Base):
    __tablename__ = "otp"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="otps")

    field_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    field_address: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    code: Mapped[int] = mapped_column(
        String(255),
        nullable=True,
    )
    used: Mapped[bool] = mapped_column(
        Boolean(),
        default=False
    )
    expired_at: Mapped[str | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[str | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=datetime.now,
    )
    updated_at: Mapped[str | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=datetime.now,
        onupdate=datetime.now,
    )
