from pydantic import BaseModel
from typing import Any

class HTTPResponse(BaseModel):
    data: Any | None = None

