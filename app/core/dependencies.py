from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id


def get_database_session():
    return Depends(get_db)


def get_current_user():
    return Depends(get_current_user_id)

