# users router

'''

uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

'''
from app.models import UserIn, UserOut, UserDb, UserBase, TokenOut, UserLoginIn
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, status, HTTPException, Header, Depends
from dataclasses import dataclass
from fastapi import APIRouter, status, HTTPException
from app.database import users
from app.auth.auth import create_access_token, Token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(userIn:UserIn):
    usersFound = [u for u in users if u.nickname == userIn.nickname]
    if len(usersFound) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    user_db = UserDb(
        id=len(users)+1,
        name=userIn.name,
        nickname=userIn.nickname,
        password=userIn.password
    )
    users.append(user_db)
@router.post(
    "/auth/",
    response_model=TokenOut,
    status_code=status.HTTP_200_OK
)
async def login(userLoginIn: UserLoginIn):
    # 1. Busco nickname y password en la peticion HTTP
    nickname: str | None = form_data.get("nickname")
    password: str | None = form_data.get("password")

    if nickname is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nickname and/or password missing"
        )

    # 2. Buscar el usuario en la "base de datos"
    usersFound = [u for u in users if u.nickname == nickname]
    if not usersFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect"
        )
    user: UserDb = usersFound[0]

    # 3. Compruebo contraseñas
    user:UserDb = usersFound[0]
    if verify_password(password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect"
        )

    token_str = create_access_token(
        UserBase(
            nickname=user.nickname,
            password=user.password
        )
    )
    return TokenOut(token=token_str)

# Get all users
@router.get("/",response_model=list[UserOut] ,status_code=status.HTTP_200_OK)
#        token=f"mytoken:{user.nickname}-{user.name}",
    

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
    
    nickname = paylaod_parts[0]
    if nickname not in [u.nickname for u in users] :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    return [UserOut(id=UserDb.id, name=UserDb.name, nickname=UserDb.nickname) for UserDb in users]
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


