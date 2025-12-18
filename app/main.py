from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

# from enum import Enum
# from pydantic import BaseModel
# from fastapi import FastAPI, Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.session import get_db
# from app.db.repositories.user import UserRepository
# from app.schemas.user import UserCreate, UserRead

# app = FastAPI()

# @app.get("/", response_model=list[UserRead])
# async def list_users(
#     db: AsyncSession = Depends(get_db),
# ):
#     repo = UserRepository(db)
#     return await repo.list()

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q" : q})
#     if not short:
#         item.update(
#             {"desc": "this is a test..."}
#         )
#     return item

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
    
    
# @app.post("/items")
# async def create_item(item: Item):
#     return item
 

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     # if model_name == ModelName.meysam:
#     return {"model name": model_name}

 