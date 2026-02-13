import mariadb
from app.models import (
    ForumIn, ForumOut, UserDb, GameDb, GameIn, GuideDb,
    MessageInstanceIn, MessageInstanceDb, ChatIn, ChatDb,
    BuildIn, BuildDb, DiscussionIn, DiscussionDb
)
from app.auth.auth import get_hash_password

db_config = {
    "host": "myapidb",  
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

# --- Forum ---
def insert_forum(forum_in: ForumIn, id_user: int, id_game: int) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO forums (name, id_game, id_user) VALUES (?, ?, ?)"
            values = (forum_in.name, id_game, id_user)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

def get_forum_by_id(forum_id: int) -> ForumOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_forum, name, id_game, id_user FROM forums WHERE id_forum = ?"
            cursor.execute(sql, (forum_id,))
            row = cursor.fetchone()
            if row:
                return ForumOut(id_forum=row[0], name=row[1], id_game=row[2], id_user=row[3])
            return None

def get_forums_by_game(game_id: int) -> list[ForumOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_forum, name, id_game, id_user FROM forums WHERE id_game = ?"
            cursor.execute(sql, (game_id,))
            rows = cursor.fetchall()
            return [ForumOut(id_forum=row[0], name=row[1], id_game=row[2], id_user=row[3]) for row in rows]

def delete_forum_by_id(forum_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM forums WHERE id_forum = ?"
            cursor.execute(sql, (forum_id,))
            conn.commit()
            return cursor.rowcount > 0

# --- User ---
def insert_user(user: UserDb) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "insert into users (name, username, email, password, image, role) values (?, ?, ?, ?, ?, ?)"
            values = (user.name, user.username, user.email, user.password, user.image, user.role)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_user_by_username(username: str) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id, name, username, email, password, image, role from users where username = ?"
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                return UserDb(id=row[0], name=row[1], username=row[2], email=row[3], password=row[4], image=row[5], role=row[6])
            return None


def get_all_users() -> list[UserDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id, name, username, email, password, image, role from users"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [UserDb(id=row[0], name=row[1], username=row[2], email=row[3], password=row[4], image=row[5], role=row[6]) for row in rows]


def delete_user_by_username(username: str) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "delete from users where username = ?"
            cursor.execute(sql, (username,))
            conn.commit()
            return cursor.rowcount > 0


users: list[UserDb] = [
    UserDb(id=1, name="dan", username="dan", email="dan@example.com", password=get_hash_password("dan"), image=None, role="admin"),
    UserDb(id=2, name="pm", username="pm", email="pm@example.com", password=get_hash_password("pm"), image=None, role="user")
]

# --- Game ---
def insert_game(game: GameIn) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "insert into games (name, gender, difficulty, rating, image, category) values (?, ?, ?, ?, ?, ?)"
            values = (game.name, game.gender, game.difficulty, game.rating, game.image, game.category)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid
        
def get_game_by_name(name: str) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id_game, name, gender, difficulty, rating, image, category from games where name = ?"
            cursor.execute(sql, (name,))
            row = cursor.fetchone()
            if row:
                return GameDb(id_game=row[0], name=row[1], gender=row[2], difficulty=row[3], rating=row[4], image=row[5], category=row[6])
            return None
        
def get_all_game() -> list[GameDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id_game, name, gender, difficulty, rating, image, category from games"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                GameDb(
                    id_game=row[0],
                    name=row[1],
                    gender=row[2],
                    difficulty=row[3],
                    rating=row[4],
                    image=row[5],
                    category=row[6]
                ) for row in rows
            ]

def update_game_by_id(game_id: int, game_in: GameIn) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE games SET name=?, gender=?, difficulty=?, rating=?, image=?, category=? WHERE id_game=?"
            values = (game_in.name, game_in.gender, game_in.difficulty, game_in.rating, game_in.image, game_in.category, game_id)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0

def delete_game_by_id(game_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM games WHERE id_game=?"
            cursor.execute(sql, (game_id,))
            conn.commit()
            return cursor.rowcount > 0

# --- Guide ---
def get_guides_by_forum(forum_id: int) -> list[GuideDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_guide, name, difficulty, category FROM guides WHERE id_forum = ?"
            cursor.execute(sql, (forum_id,))
            rows = cursor.fetchall()
            return [GuideDb(id_guide=row[0], name=row[1], difficulty=row[2], category=row[3]) for row in rows]

def get_all_guides() -> list[GuideDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_guide, name, difficulty, category FROM guides"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [GuideDb(id_guide=row[0], name=row[1], difficulty=row[2], category=row[3]) for row in rows]

def get_guide_by_id(guide_id: int) -> GuideDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_guide, name, difficulty, category FROM guides WHERE id_guide = ?"
            cursor.execute(sql, (guide_id,))
            row = cursor.fetchone()
            if row:
                return GuideDb(id_guide=row[0], name=row[1], difficulty=row[2], category=row[3])
            return None

def delete_guide(guide_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM guides WHERE id_guide = ?"
            cursor.execute(sql, (guide_id,))
            conn.commit()
            return cursor.rowcount > 0

# --- MessagesInstance ---
def insert_message_instance(message_in: MessageInstanceIn) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO messages_instance (status, content) VALUES (?, ?)"
            values = (message_in.status, message_in.content)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

def get_message_instance_by_id(id_mi: int) -> MessageInstanceDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_mi, status, content, timestamp FROM messages_instance WHERE id_mi = ?"
            cursor.execute(sql, (id_mi,))
            row = cursor.fetchone()
            if row:
                return MessageInstanceDb(id_mi=row[0], status=row[1], content=row[2], timestamp=str(row[3]) if row[3] else None)
            return None

def get_all_messages_instance() -> list[MessageInstanceDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_mi, status, content, timestamp FROM messages_instance"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [MessageInstanceDb(id_mi=row[0], status=row[1], content=row[2], timestamp=str(row[3]) if row[3] else None) for row in rows]

def delete_message_instance(id_mi: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM messages_instance WHERE id_mi = ?"
            cursor.execute(sql, (id_mi,))
            conn.commit()
            return cursor.rowcount > 0

# --- Chat ---
def insert_chat(chat_in: ChatIn) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO chat (id_mi, content) VALUES (?, ?)"
            values = (chat_in.id_mi, chat_in.content)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

def get_chat_by_id(id_chat: int) -> ChatDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_chat, id_mi, content, timestamp FROM chat WHERE id_chat = ?"
            cursor.execute(sql, (id_chat,))
            row = cursor.fetchone()
            if row:
                return ChatDb(id_chat=row[0], id_mi=row[1], content=row[2], timestamp=str(row[3]) if row[3] else None)
            return None

def get_chats_by_message_instance(id_mi: int) -> list[ChatDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_chat, id_mi, content, timestamp FROM chat WHERE id_mi = ?"
            cursor.execute(sql, (id_mi,))
            rows = cursor.fetchall()
            return [ChatDb(id_chat=row[0], id_mi=row[1], content=row[2], timestamp=str(row[3]) if row[3] else None) for row in rows]

def get_all_chats() -> list[ChatDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_chat, id_mi, content, timestamp FROM chat"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [ChatDb(id_chat=row[0], id_mi=row[1], content=row[2], timestamp=str(row[3]) if row[3] else None) for row in rows]

def delete_chat(id_chat: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM chat WHERE id_chat = ?"
            cursor.execute(sql, (id_chat,))
            conn.commit()
            return cursor.rowcount > 0

# --- Build ---
def insert_build(build_in: BuildIn) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO builds (name, planner, category, description, id_forum) VALUES (?, ?, ?, ?, ?)"
            values = (build_in.name, build_in.planner, build_in.category, build_in.description, build_in.id_forum)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

def get_build_by_id(id_build: int) -> BuildDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_build, name, planner, category, description, id_forum FROM builds WHERE id_build = ?"
            cursor.execute(sql, (id_build,))
            row = cursor.fetchone()
            if row:
                return BuildDb(id_build=row[0], name=row[1], planner=row[2], category=row[3], description=row[4], id_forum=row[5])
            return None

def get_all_builds() -> list[BuildDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_build, name, planner, category, description, id_forum FROM builds"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [BuildDb(id_build=row[0], name=row[1], planner=row[2], category=row[3], description=row[4], id_forum=row[5]) for row in rows]

def get_builds_by_forum(id_forum: int) -> list[BuildDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_build, name, planner, category, description, id_forum FROM builds WHERE id_forum = ?"
            cursor.execute(sql, (id_forum,))
            rows = cursor.fetchall()
            return [BuildDb(id_build=row[0], name=row[1], planner=row[2], category=row[3], description=row[4], id_forum=row[5]) for row in rows]

def update_build(id_build: int, build_in: BuildIn) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE builds SET name=?, planner=?, category=?, description=?, id_forum=? WHERE id_build=?"
            values = (build_in.name, build_in.planner, build_in.category, build_in.description, build_in.id_forum, id_build)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0

def delete_build(id_build: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM builds WHERE id_build = ?"
            cursor.execute(sql, (id_build,))
            conn.commit()
            return cursor.rowcount > 0

# --- Discussion functions ---
def insert_discussion(discussion_in: DiscussionIn, id_user: int) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO discussion (name, comments, posts, rating, id_forum, id_user) VALUES (?, ?, ?, ?, ?, ?)"
            values = (discussion_in.name, discussion_in.comments, discussion_in.posts, discussion_in.rating, discussion_in.id_forum, id_user)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

def get_discussion_by_id(id_discussion: int) -> DiscussionDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_discussion, name, comments, posts, rating, id_forum, id_user FROM discussion WHERE id_discussion = ?"
            cursor.execute(sql, (id_discussion,))
            row = cursor.fetchone()
            if row:
                return DiscussionDb(id_discussion=row[0], name=row[1], comments=row[2], posts=row[3], rating=float(row[4]) if row[4] else None, id_forum=row[5], id_user=row[6])
            return None

def get_all_discussions() -> list[DiscussionDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_discussion, name, comments, posts, rating, id_forum, id_user FROM discussion"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [DiscussionDb(id_discussion=row[0], name=row[1], comments=row[2], posts=row[3], rating=float(row[4]) if row[4] else None, id_forum=row[5], id_user=row[6]) for row in rows]

def get_discussions_by_forum(id_forum: int) -> list[DiscussionDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_discussion, name, comments, posts, rating, id_forum, id_user FROM discussion WHERE id_forum = ?"
            cursor.execute(sql, (id_forum,))
            rows = cursor.fetchall()
            return [DiscussionDb(id_discussion=row[0], name=row[1], comments=row[2], posts=row[3], rating=float(row[4]) if row[4] else None, id_forum=row[5], id_user=row[6]) for row in rows]

def update_discussion(id_discussion: int, discussion_in: DiscussionIn) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE discussion SET name=?, comments=?, posts=?, rating=?, id_forum=? WHERE id_discussion=?"
            values = (discussion_in.name, discussion_in.comments, discussion_in.posts, discussion_in.rating, discussion_in.id_forum, id_discussion)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0

def delete_discussion(id_discussion: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM discussion WHERE id_discussion = ?"
            cursor.execute(sql, (id_discussion,))
            conn.commit()
            return cursor.rowcount > 0

