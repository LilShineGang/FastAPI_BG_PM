from app.models import UserDb
import mariadb

db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

def insert_user(user: UserDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "insert into users (name, username, password) values (?, ?, ?)"
            values = (user.name, user.username, user.password)
            cursor.execute(
                sql,
                values
            )
            conn.commit()
            return cursor.lastrowid


def get_user_by_username(username: str) -> UserDb | None:
    #TODO terminar esta funcion
    return None

users: list[UserDb] = [
    UserDb(id=1, name="dan", username="dan", password="$2b$12$Qfdl34mplZu6aQvCttEj.OcjirEgd2w92Zzcyzb7LZNIqA3bPusEe"),
    UserDb(id=2, name="pm", username="pm", password="pm")
]