from pydantic import BaseModel

class UserBase(BaseModel):
    username:str
    password:str

class UserIn(UserBase):
    name:str
    email:str
    image:str | None = None

class UserDb(UserIn):
    id:int

class UserOut(BaseModel):
    id:int
    name:str
    username:str
    email:str
    image:str | None = None

#class UserLoginIn(UserBase):
#    pass

class TokenOut(BaseModel):
    token:str

# --- Game models ---
class GameIn(BaseModel):
    name: str
    gender: str
    difficulty: str
    rating: float | None = None
    image: str | None = None
    category: str

class GameDb(GameIn):
    id_game: int

class GameOut(BaseModel):
    id_game: int
    name: str
    gender: str
    difficulty: str
    rating: float | None = None
    image: str | None = None
    category: str
