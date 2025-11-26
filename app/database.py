from app.models import UserDb


users: list[UserDb] = [
    UserDb(id=1, name="dan", username="dan", password="$2b$12$Qfdl34mplZu6aQvCttEj.OcjirEgd2w92Zzcyzb7LZNIqA3bPusEe"),
    UserDb(id=2, name="pm", username="pm", password="pm")
]