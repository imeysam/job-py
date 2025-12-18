from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Literal
import re
from typing_extensions import Self
from datetime import datetime


class MobileRule:
    """Custom validator for mobile numbers"""

    @staticmethod
    def validate(value: str) -> str:
        # Add your mobile number validation logic here
        # Example: validate as a phone number with country code
        if not value:
            raise ValueError("Mobile number is required")
        # Simple validation - you should replace with proper phone validation
        if not re.match(r"^09\d{9}$", value):
            raise ValueError("Invalid mobile number format")
        return value


class EmailRule:
    """Custom validator for email address"""

    @staticmethod
    def validate(value: str) -> str:
        if len(value) > 255:
            raise ValueError("Email address must not exceed 255 characters")
            # Basic email format check (Pydantic's EmailStr does this better)
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format")
        return value


class OTPCreate(BaseModel):
    field: Literal["mobile", "email"]
    address: Annotated[str, Field(..., min_length=1)]

    # @model_validator(mode='before')
    # @classmethod
    # def validate_address_based_on_type(cls, data: Any) -> Any:
    #     if data.get('field') == "mobile":
    #         if not re.match(r"^09\d{9}$", data.get('address')):
    #             raise ValueError(
    #                 "Mobile number must be in format: 09xxxxxxxxx "
    #                 "(09 followed by 9 digits, total 11 digits)"
    #             )
    #     else:
    #         email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    #         if not re.match(email_pattern, data.get('address')):
    #             raise ValueError("Address must be a valid email")
    #     return data

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.field == "mobile":
            MobileRule.validate(self.address)
        else:
            EmailRule.validate(self.address)
        return self


class OTPVerify(BaseModel):
    field: Literal["mobile", "email"]
    otp: Annotated[
        int,
        Field(..., ge=111111, le=999999, description="OTP must be a 6-digit number"),
    ]
    address: Annotated[str, Field(..., min_length=1)]

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.field == "mobile":
            MobileRule.validate(self.address)
        else:
            EmailRule.validate(self.address)
        return self


class OTPRead(BaseModel):
    code: str
    used: bool
    expired_at: datetime


class OTPUpdate(BaseModel):
    used: bool
