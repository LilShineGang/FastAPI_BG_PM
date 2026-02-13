# --- Forum database functions ---
from app.models import ForumIn, ForumOut



import mariadb

import mariadb
from app.models import (
    AchievementIn,
    AchievementOut,
    ForumIn,
    ForumOut,
    GameDb,
    GameIn,
    GroupIn,
    GroupOut,
    TierListIn,
    TierListOut,
    UserDb,
    WikiIn,
    WikiOut,
)
from app.auth.auth import get_hash_password
from app.models import GameDb, GameIn, UserDb

db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi",
}


def insert_user(user: UserDb) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "insert into users (name, username, email, password, image, role) values (?, ?, ?, ?, ?, ?)"
            values = (
                user.name,
                user.username,
                user.email,
                user.password,
                user.image,
                user.role,
            )
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
                return UserDb(
                    id=row[0],
                    name=row[1],
                    username=row[2],
                    email=row[3],
                    password=row[4],
                    image=row[5],
                    role=row[6],
                )
            return None


def get_all_users() -> list[UserDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id, name, username, email, password, image, role from users"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                UserDb(
                    id=row[0],
                    name=row[1],
                    username=row[2],
                    email=row[3],
                    password=row[4],
                    image=row[5],
                    role=row[6],
                )
                for row in rows
            ]


def delete_user_by_username(username: str) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "delete from users where username = ?"
            cursor.execute(sql, (username,))
            conn.commit()
            return cursor.rowcount > 0


users: list[UserDb] = [
    UserDb(
        id=1,
        name="dan",
        username="dan",
        email="dan@example.com",
        password=get_hash_password("dan"),
        image=None,
        role="admin",
    ),
    UserDb(
        id=2,
        name="pm",
        username="pm",
        email="pm@example.com",
        password=get_hash_password("pm"),
        image=None,
        role="user",
    ),
]


def insert_game(game: GameIn) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "insert into games (name, gender, difficulty, rating, image, category) values (?, ?, ?, ?, ?, ?)"
            values = (
                game.name,
                game.gender,
                game.difficulty,
                game.rating,
                game.image,
                game.category,
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_game_by_name(name: str) -> GameDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id_game, name, gender, difficulty, rating, image, category from games where name = ?"
            cursor.execute(sql, (name,))
            row = cursor.fetchone()
            if row:
                return GameDb(
                    id_game=row[0],
                    name=row[1],
                    gender=row[2],
                    difficulty=row[3],
                    rating=row[4],
                    image=row[5],
                    category=row[6],
                )
            return None


def get_game_by_id(game_id: int) -> GameDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id_game, name, gender, difficulty, rating, image, category from games where id_game = ?"
            cursor.execute(sql, (game_id,))
            row = cursor.fetchone()
            if row:
                return GameDb(
                    id_game=row[0],
                    name=row[1],
                    gender=row[2],
                    difficulty=row[3],
                    rating=row[4],
                    image=row[5],
                    category=row[6],
                )
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
                    category=row[6],
                )
                for row in rows
            ]


def update_game_by_id(game_id: int, game_in: GameIn) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE games SET name=?, gender=?, difficulty=?, rating=?, image=?, category=? WHERE id_game=?"
            values = (
                game_in.name,
                game_in.gender,
                game_in.difficulty,
                game_in.rating,
                game_in.image,
                game_in.category,
                game_id,
            )
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


# --- Guide database functions ---


def get_guide_by_id(guide_id: int):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_guide, name, difficulty, category, id_user, id_forum FROM guides WHERE id_guide = ?"
            cursor.execute(sql, (guide_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id_guide": row[0],
                    "name": row[1],
                    "difficulty": row[2],
                    "category": row[3],
                    "id_user": row[4],
                    "id_forum": row[5],
                }
            return None


def insert_guide(guide_in, id_user, id_forum) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO guides (name, difficulty, category, id_user, id_forum) VALUES (?, ?, ?, ?, ?)"
            values = (
                guide_in.name,
                guide_in.difficulty,
                guide_in.category,
                id_user,
                id_forum,
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

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
        

def insert_wiki(wiki_in: WikiIn) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO wiki (name, category, description, id_forum) VALUES (?, ?, ?, ?)"
            values = (wiki_in.name, wiki_in.category, wiki_in.description, wiki_in.id_forum)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def delete_guide_by_id(guide_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM guides WHERE id_guide = ?"
            cursor.execute(sql, (guide_id,))
            conn.commit()
            return cursor.rowcount > 0


def get_guides_by_forum(forum_id: int) -> list[dict]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_guide, name, difficulty, category, id_user, id_forum FROM guides WHERE id_forum = ?"
            cursor.execute(sql, (forum_id,))
            rows = cursor.fetchall()
            return [
                {
                    "id_guide": row[0],
                    "name": row[1],
                    "difficulty": row[2],
                    "category": row[3],
                    "id_user": row[4],
                    "id_forum": row[5],
                }
                for row in rows
            ]
def get_wiki_by_id(wiki_id: int) -> WikiOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_wiki, name, category, description, id_forum FROM wiki WHERE id_wiki = ?"
            cursor.execute(sql, (wiki_id,))
            row = cursor.fetchone()
            if row:
                return WikiOut(
                    id_wiki=row[0],
                    name=row[1],
                    category=row[2],
                    description=row[3],
                    id_forum=row[4]
                )
            return None

def get_all_wiki() -> list[WikiOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_wiki, name, category, description, id_forum FROM wiki"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                WikiOut(
                    id_wiki=row[0],
                    name=row[1],
                    category=row[2],
                    description=row[3],
                    id_forum=row[4]
                ) for row in rows
            ]

def get_wikis_by_forum(forum_id: int) -> list[WikiOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_wiki, name, category, description, id_forum FROM wiki WHERE id_forum = ?"
            cursor.execute(sql, (forum_id,))
            rows = cursor.fetchall()
            return [
                WikiOut(
                    id_wiki=row[0],
                    name=row[1],
                    category=row[2],
                    description=row[3],
                    id_forum=row[4]
                ) for row in rows
            ]

def update_wiki_by_id(wiki_id: int, wiki_in: WikiIn) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE wiki SET name=?, category=?, description=?, id_forum=? WHERE id_wiki=?"
            values = (wiki_in.name, wiki_in.category, wiki_in.description, wiki_in.id_forum, wiki_id)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0

def delete_wiki_by_id(wiki_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM wiki WHERE id_wiki = ?"
            cursor.execute(sql, (wiki_id,))
            conn.commit()
            return cursor.rowcount > 0


# --- Tier list database functions ---


def insert_tier_list(tier_list_in: TierListIn) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO tier_list (name, category, description, id_forum) VALUES (?, ?, ?, ?)"
            values = (
                tier_list_in.name,
                tier_list_in.category,
                tier_list_in.description,
                tier_list_in.id_forum,
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_tier_list_by_id(tier_list_id: int) -> TierListOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_tl, name, category, description, id_forum FROM tier_list WHERE id_tl = ?"
            cursor.execute(sql, (tier_list_id,))
            row = cursor.fetchone()
            if row:
                return TierListOut(
                    id_tl=row[0],
                    name=row[1],
                    category=row[2],
                    description=row[3],
                    id_forum=row[4],
                )
            return None


def get_all_tier_list() -> list[TierListOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_tl, name, category, description, id_forum FROM tier_list"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                TierListOut(
                    id_tl=row[0],
                    name=row[1],
                    category=row[2],
                    description=row[3],
                    id_forum=row[4],
                )
                for row in rows
            ]


def get_tier_lists_by_forum(forum_id: int) -> list[TierListOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_tl, name, category, description, id_forum FROM tier_list WHERE id_forum = ?"
            cursor.execute(sql, (forum_id,))
            rows = cursor.fetchall()
            return [
                TierListOut(
                    id_tl=row[0],
                    name=row[1],
                    category=row[2],
                    description=row[3],
                    id_forum=row[4],
                )
                for row in rows
            ]


def update_tier_list_by_id(tier_list_id: int, tier_list_in: TierListIn) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE tier_list SET name = ?, category = ?, description = ?, id_forum = ? WHERE id_tl = ?"
            values = (
                tier_list_in.name,
                tier_list_in.category,
                tier_list_in.description,
                tier_list_in.id_forum,
                tier_list_id,
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0


def delete_tier_list_by_id(tier_list_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM tier_list WHERE id_tl = ?"
            cursor.execute(sql, (tier_list_id,))
            conn.commit()
            return cursor.rowcount > 0


# --- Achievement database functions ---


def insert_achievement(achievement_in: AchievementIn) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "INSERT INTO achievement (difficulty, description, id_game) VALUES (?, ?, ?)"
            values = (
                achievement_in.difficulty,
                achievement_in.description,
                achievement_in.id_game,
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_achievement_by_id(achievement_id: int) -> AchievementOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_achievement, difficulty, description, id_game FROM achievement WHERE id_achievement = ?"
            cursor.execute(sql, (achievement_id,))
            row = cursor.fetchone()
            if row:
                return AchievementOut(
                    id_achievement=row[0],
                    difficulty=row[1],
                    description=row[2],
                    id_game=row[3],
                )
            return None


def get_all_achievements() -> list[AchievementOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_achievement, difficulty, description, id_game FROM achievement"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                AchievementOut(
                    id_achievement=row[0],
                    difficulty=row[1],
                    description=row[2],
                    id_game=row[3],
                )
                for row in rows
            ]


def get_achievements_by_game(game_id: int) -> list[AchievementOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_achievement, difficulty, description, id_game FROM achievement WHERE id_game = ?"
            cursor.execute(sql, (game_id,))
            rows = cursor.fetchall()
            return [
                AchievementOut(
                    id_achievement=row[0],
                    difficulty=row[1],
                    description=row[2],
                    id_game=row[3],
                )
                for row in rows
            ]


def update_achievement_by_id(achievement_id: int, achievement_in: AchievementIn) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "UPDATE achievement SET difficulty = ?, description = ?, id_game = ? WHERE id_achievement = ?"
            values = (
                achievement_in.difficulty,
                achievement_in.description,
                achievement_in.id_game,
                achievement_id,
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0


def delete_achievement_by_id(achievement_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM achievement WHERE id_achievement = ?"
            cursor.execute(sql, (achievement_id,))
            conn.commit()
            return cursor.rowcount > 0


# --- Groups database functions ---


def insert_group(group_in: GroupIn, admin_id: int) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = (
                "INSERT INTO groups_table (name, admin, description, image, id_forum) "
                "VALUES (?, ?, ?, ?, ?)"
            )
            values = (
                group_in.name,
                admin_id,
                group_in.description,
                group_in.image,
                group_in.id_forum,
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_group_by_id(group_id: int) -> GroupOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = (
                "SELECT id_group, name, admin, description, image, id_forum "
                "FROM groups_table WHERE id_group = ?"
            )
            cursor.execute(sql, (group_id,))
            row = cursor.fetchone()
            if row:
                return GroupOut(
                    id_group=row[0],
                    name=row[1],
                    admin=row[2],
                    description=row[3],
                    image=row[4],
                    id_forum=row[5],
                )
            return None


def get_all_groups() -> list[GroupOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id_group, name, admin, description, image, id_forum FROM groups_table"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [
                GroupOut(
                    id_group=row[0],
                    name=row[1],
                    admin=row[2],
                    description=row[3],
                    image=row[4],
                    id_forum=row[5],
                )
                for row in rows
            ]


def get_groups_by_forum(forum_id: int) -> list[GroupOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = (
                "SELECT id_group, name, admin, description, image, id_forum "
                "FROM groups_table WHERE id_forum = ?"
            )
            cursor.execute(sql, (forum_id,))
            rows = cursor.fetchall()
            return [
                GroupOut(
                    id_group=row[0],
                    name=row[1],
                    admin=row[2],
                    description=row[3],
                    image=row[4],
                    id_forum=row[5],
                )
                for row in rows
            ]


def update_group_by_id(group_id: int, group_in: GroupIn) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = (
                "UPDATE groups_table SET name = ?, description = ?, image = ?, id_forum = ? "
                "WHERE id_group = ?"
            )
            values = (
                group_in.name,
                group_in.description,
                group_in.image,
                group_in.id_forum,
                group_id,
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0


def delete_group_by_id(group_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM groups_table WHERE id_group = ?"
            cursor.execute(sql, (group_id,))
            conn.commit()
            return cursor.rowcount > 0
