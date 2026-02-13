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

# --- Guide models ---
class GuideIn(BaseModel):
    name: str
    difficulty: str
    category: str

class GuideDb(GuideIn):
    id_guide: int

class GuideOut(BaseModel):
    id_guide: int
    name: str
    difficulty: str
    category: str

# --- MessagesInstance models ---
class MessageInstanceIn(BaseModel):
    status: str
    content: str | None = None

class MessageInstanceDb(MessageInstanceIn):
    id_mi: int
    timestamp: str | None = None

class MessageInstanceOut(BaseModel):
    id_mi: int
    status: str
    content: str | None = None
    timestamp: str | None = None

# --- Chat models ---
class ChatIn(BaseModel):
    id_mi: int
    content: str

class ChatDb(ChatIn):
    id_chat: int
    timestamp: str | None = None

class ChatOut(BaseModel):
    id_chat: int
    id_mi: int
    content: str
    timestamp: str | None = None

# --- Build models ---
class BuildIn(BaseModel):
    name: str
    planner: str
    category: str
    description: str
    id_forum: int | None = None

class BuildDb(BuildIn):
    id_build: int

class BuildOut(BaseModel):
    id_build: int
    name: str
    planner: str
    category: str
    description: str
    id_forum: int | None = None

# --- Discussion models ---
class DiscussionIn(BaseModel):
    name: str
    comments: str | None = None
    posts: int | None = None
    rating: float | None = None
    id_forum: int | None = None

class DiscussionDb(DiscussionIn):
    id_discussion: int

class DiscussionOut(BaseModel):
    id_discussion: int
    name: str
    comments: str | None = None
    posts: int | None = None
    rating: float | None = None
    id_forum: int | None = None
    id_user: int | None = None