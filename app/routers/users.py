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

# Get all users
@router.get("/",response_model=list[UserOut] ,status_code=status.HTTP_200_OK)
async def get_all_users(authorization: str | None = Header()):
    print(authorization)
    
    parts = authorization.split(":") # Separamos mytoken de lo demas
    if len(parts) !=2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    if parts[0] != "mytoken": # Verificar el token
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    paylaod_parts = parts[1].split("--")
    if len(paylaod_parts) !=2: # Separamos nickname de name
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    username = paylaod_parts[0]
    if username not in [u.username for u in users] :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    return [UserOut(id=UserDb.id, name=UserDb.name, username=UserDb.username) for UserDb in users]
    #tecnicamente es lo mismo que: "return users" ya que FastAPI se encarga de hacer el filtrado poniendole el response_model



# Payload
# ---------
# {
#   "sub": "nombre" (emisor del token)
#   "iss": "..." --no hace falta por ahora pero es el emisor del token
#   "exp": "tiempo de expiracion del token"
# }
#
# Signature
# ----------
# Se coge el header, el paylode y se aplica el codigo secreto.
#
# HM...(
#   base64UrlEncode(header) + "." + base64UrlEncode(payload), secret
# )
#


