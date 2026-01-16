import mariadb
from app.models import UserDb, GameDb, GameIn
from app.auth.auth import get_hash_password

db_config = {
    "host": "myapidb",  
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

def insert_user(user: UserDb) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "insert into users (name, username, email, password, image) values (?, ?, ?, ?, ?)"
            values = (user.name, user.username, user.email, user.password, user.image)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def get_user_by_username(username: str) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id, name, username, email, password, image from users where username = ?"
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                return UserDb(id=row[0], name=row[1], username=row[2], email=row[3], password=row[4], image=row[5])
            return None


def get_all_users() -> list[UserDb]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "select id, name, username, email, password, image from users"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [UserDb(id=row[0], name=row[1], username=row[2], email=row[3], password=row[4], image=row[5]) for row in rows]


def delete_user_by_username(username: str) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "delete from users where username = ?"
            cursor.execute(sql, (username,))
            conn.commit()
            return cursor.rowcount > 0


users: list[UserDb] = [
    UserDb(id=1, name="dan", username="dan", email="dan@example.com", password=get_hash_password("dan"), image=None),
    UserDb(id=2, name="pm", username="pm", email="pm@example.com", password=get_hash_password("pm"), image=None)
]

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