from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    field: str
    address: str

class UserRead(BaseModel):
    id: int
    mobile: str | None
    email: EmailStr | None
    first_name: str | None
    last_name: str | None

    model_config = ConfigDict(from_attributes=True)
