from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User as UserModel
from app.database.core import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


class UserSchemaBase(BaseModel):
    email: str | None = None
    name: str | None = None


class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    id: str

    class Config:
        orm_mode = True


@router.post("/users", response_model=UserSchema)
async def create_user(
    user: UserSchemaCreate, db: AsyncSession = Depends(get_db)
) -> UserModel:
    user = await UserModel.create(db, **user.dict())
    return user


@router.get("/users", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[UserModel]:
    users = await UserModel.get_all(db)
    return users
