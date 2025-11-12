# users router

from pydantic import BaseModel
from dataclasses import dataclass
from fastapi import APIRouter, status, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

class UserBase(BaseModel):
    nickname:str
    password:str

class UserIn(UserBase):
    name:str

class UserDb(UserIn):
    id:int

class UserLogin(UserBase):
    pass

users:list[UserDb] = []

class TokenOut(BaseModel):
    token:str

@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def create_user(userIn:UserIn):
    in len(usersFound) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    users.append(
        UserDb(
            id=len(users)+1,
            name=userIn.name,
            nickname=userIn.nickname,
            password=userIn.password
        )
    )

@router.post(
    "/auth/",
    response_model=TokenOut,
    status_code=status.HTTP_200_OK
)
async def login(userLoginIn:UserLogin):
    usersFound = [u for u in users if u.username == userLoginIn.username]
    if not usersFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect"
        )
    user: UserDb=usersFound[0]

    if user.password != userLoginIn.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect"
        )

    return TokenOut(
        token=f"mytoken:{user.nickname}-{user.name}",
    )


