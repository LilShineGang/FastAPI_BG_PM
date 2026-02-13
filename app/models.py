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
    username: str
    password: str


class UserIn(UserBase):
    name: str
    email: str
    image: str | None = None
    role: str = "user"


class UserDb(UserIn):
    id: int


class UserOut(BaseModel):
    id: int
    name: str
    username: str
    email: str
    image: str | None = None
    role: str


# class UserLoginIn(UserBase):
#    pass


class TokenOut(BaseModel):
    token: str


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


class AchievementIn(BaseModel):
    difficulty: str
    description: str
    id_game: int | None = None

# --- Archivements models ---
class AchievementDb(AchievementIn):
    id_achievement: int


class AchievementOut(BaseModel):
    id_achievement: int
    difficulty: str
    description: str
    id_game: int | None = None

# --- GUides models ---
class GuideIn(BaseModel):
    name: str
    difficulty: str
    category: str
    forum_id: int


class GuideOut(BaseModel):
    id_guide: int
    name: str
    difficulty: str
    category: str
# --- Forum models ---
class ForumIn(BaseModel):
    name: str
    game_name: str


class ForumOut(BaseModel):
    id_forum: int
    name: str
    id_game: int | None = None
    id_user: int | None = None

# --- Wiki models ---

class WikiIn(BaseModel):
    name: str
    category: str
    description: str
    id_forum: int | None = None

class WikiOut(BaseModel):
    id_wiki: int
    name: str
    category: str
    description: str
    id_forum: int | None = None


# --- Tier list models ---


class TierListIn(BaseModel):
    name: str
    category: str
    description: str
    id_forum: int | None = None


class TierListOut(BaseModel):
    id_tl: int
    name: str
    category: str
    description: str
    id_forum: int | None = None


# --- Groups models ---


class GroupIn(BaseModel):
    name: str
    description: str | None = None
    image: str | None = None
    id_forum: int | None = None


class GroupOut(BaseModel):
    id_group: int
    name: str
    admin: int
    description: str | None = None
    image: str | None = None
    id_forum: int | None = None
