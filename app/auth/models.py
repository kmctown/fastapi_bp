from typing import Any

import bcrypt
from sqlalchemy import BigInteger, Boolean, Column, LargeBinary, String, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.core import Base
from app.models import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(LargeBinary(60))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs: dict[str, Any]) -> "User":
        user = cls(**kwargs)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list["User"]:
        result = await db.execute(select(cls))  # type: ignore
        return result.scalars().all()

    def hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    def set_password(self, password: str) -> None:
        self.password = self.hash_password(password)

    def check_password(self, password: str) -> bool:
        if not self.password:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password)
