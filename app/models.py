from pydantic import BaseModel

class UserBase(BaseModel):
    username:str
    password:str

class UserIn(UserBase):
    name:str
    email:str
    image:str | None = None

class UserDb(UserIn):
    id_user:int

class UserOut(BaseModel):
    id_user:int
    name:str
    username:str
    email:str
    image:str | None = None

#class UserLoginIn(UserBase):
#    pass
    
class TokenOut(BaseModel):
    token:str

# Game Models
class GameBase(BaseModel):
    name: str
    gender: str
    difficulty: str
    category: str
    rating: float | None = None
    image: str | None = None

class GameIn(GameBase):
    pass

class GameDb(GameBase):
    id_game: int

class GameOut(BaseModel):
    id_game: int
    name: str
    gender: str
    difficulty: str
    rating: float | None = None
    image: str | None = None
    category: str
