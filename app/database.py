import mariadb
from app.models import UserDb
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