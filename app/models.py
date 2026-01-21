from pydantic import BaseModel

# --- Forum models ---
class ForumIn(BaseModel):
    name: str
    game_name: str

class ForumOut(BaseModel):
    id_forum: int
    name: str
    id_game: int | None = None
    id_user: int | None = None

class UserBase(BaseModel):
    username:str
    password:str

class UserIn(UserBase):
    name:str
    email:str
    image:str | None = None
    role: str = 'user'

class UserDb(UserIn):
    id:int

class UserOut(BaseModel):
    id:int
    name:str
    username:str
    email:str
    image:str | None = None
    role: str

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
