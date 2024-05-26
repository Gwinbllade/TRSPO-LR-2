from typing import List

from fastapi import APIRouter, HTTPException, Depends

from app.users.dao import UserDAO
from app.users.models import UserRole
from app.users.shemas import SUser, SUserAuth, SUserUpdate

router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.get("")
async def get_users() -> List[SUser]:
    users = await UserDAO.find_all()
    return users


@router.get("/{user_id}")
async def get_user(user_id: int) -> SUser:
    user = await UserDAO.find_one_or_none(id=user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/register")
async def register(user_data: SUserAuth = Depends()) -> SUser:
    existing_user = await UserDAO.find_all(email=user_data.email)
    if len(existing_user) != 0:
        raise HTTPException(status_code=500, detail="Email already registered")
    else:
        new_user = await UserDAO.add(email=user_data.email,
                          hashed_password=user_data.password,
                          username=user_data.username,
                          role="buyer")
        return new_user


@router.patch("")
async def update(user_data: SUserUpdate = Depends()) -> SUser:
    user = await UserDAO.find_by_id(user_data.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.dict(exclude_none=True)
    if update_data.get("password"):
        update_data["hashed_password"] = update_data.pop("password")

    try:    
        updated_user = await UserDAO.update(filter_by={"id": user_data.id}, **update_data)
        return updated_user
    except:
        raise HTTPException(status_code=500, detail="Failed to update user")


