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

<<<<<<< HEAD

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
=======
# --- Guide models ---
>>>>>>> d5f2d159d5ade8423f85afd3da65c6ac6722c5f8
class GuideIn(BaseModel):
    name: str
    difficulty: str
    category: str
<<<<<<< HEAD
    forum_id: int

=======

class GuideDb(GuideIn):
    id_guide: int
>>>>>>> d5f2d159d5ade8423f85afd3da65c6ac6722c5f8

class GuideOut(BaseModel):
    id_guide: int
    name: str
    difficulty: str
    category: str
<<<<<<< HEAD
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
=======

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
>>>>>>> d5f2d159d5ade8423f85afd3da65c6ac6722c5f8
    category: str
    description: str
    id_forum: int | None = None

<<<<<<< HEAD
class WikiOut(BaseModel):
    id_wiki: int
    name: str
=======
class BuildDb(BuildIn):
    id_build: int

class BuildOut(BaseModel):
    id_build: int
    name: str
    planner: str
>>>>>>> d5f2d159d5ade8423f85afd3da65c6ac6722c5f8
    category: str
    description: str
    id_forum: int | None = None

<<<<<<< HEAD

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
=======
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
>>>>>>> d5f2d159d5ade8423f85afd3da65c6ac6722c5f8
