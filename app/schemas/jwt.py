from pydantic import BaseModel

class JWTToken(BaseModel):
    access: str
    exp: int
