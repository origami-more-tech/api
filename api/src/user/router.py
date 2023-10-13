from fastapi import APIRouter
from user.model import User
from contstants import Collection


router = APIRouter()
router.tags = [Collection.user]


@router.get("/auth")
async def get_user() -> User:
    return User()
