from abc import ABC
from fastapi import status, HTTPException
from typing import Dict, Annotated
from app.utils.logger import logger

# from telebot import TeleBot
# from utils.bot_helpers import BotMessageSender
# from setting import BOT_TOKEN


class CustomHTTPException(ABC, HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error: Annotated[str | None, "Error message for logging"] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        if error:
            logger.error(f"{self.status_code}: {error}")
        # self.headers = {"Content-Type": "application/json"}

    def __repr__(self) -> Dict:
        return {"message": self.detail}


class BadRequestException(CustomHTTPException):
    def __init__(
        self,
        detail: str = "Bad Request.",
        error: Annotated[str | None, "Error message for logging"] = None,
    ) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(status_code=self.status_code, detail=detail, error=error)


class UnauthorizedException(CustomHTTPException):
    def __init__(
        self,
        detail: str = "Unauthorized.",
        error: Annotated[str | None, "Error message for logging"] = None,
    ) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code=self.status_code, detail=detail, error=error)


class ForbiddenException(CustomHTTPException):
    def __init__(
        self,
        detail: str = "Forbidden.",
        error: Annotated[str | None, "Error message for logging"] = None,
    ) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        super().__init__(status_code=self.status_code, detail=detail, error=error)


class NotFoundException(CustomHTTPException):
    def __init__(
        self,
        detail: str = "Not Found.",
        error: Annotated[str | None, "Error message for logging"] = None,
    ) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code=self.status_code, detail=detail, error=error)


class ConflictException(CustomHTTPException):
    def __init__(
        self,
        detail: str = "Conflict.",
        error: Annotated[str | None, "Error message for logging"] = None,
    ) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(status_code=self.status_code, detail=detail, error=error)


class UnprocessableEntityException(CustomHTTPException):
    def __init__(
        self,
        detail: str = "Unprocessable Entity.",
        error: Annotated[str | None, "Error message for logging"] = None,
    ) -> None:
        self.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        super().__init__(status_code=self.status_code, detail=detail, error=error)
