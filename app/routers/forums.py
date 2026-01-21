from fastapi import APIRouter, status, Depends, HTTPException
from app.models import ForumIn, ForumOut
from app.database import insert_forum, get_forum_by_id, get_forums_by_game, delete_forum_by_id, get_user_by_username, get_game_by_name
from app.auth.auth import oauth2_scheme, decode_token, TokenData

router = APIRouter(
    prefix="/forums",
    tags=["Forums"]
)

# Crear un nuevo foro
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ForumOut)
async def create_forum(forum_in: ForumIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    game = get_game_by_name(forum_in.game_name)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    forum_id = insert_forum(forum_in, user.id, game.id_game)
    return ForumOut(id_forum=forum_id, name=forum_in.name, id_game=game.id_game, id_user=user.id)

# Obtener todos los foros de un juego
@router.get("/game/{game_id}/", response_model=list[ForumOut])
async def get_forums(game_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    forums = get_forums_by_game(game_id)
    return forums

# Obtener un foro por id
@router.get("/{forum_id}/", response_model=ForumOut)
async def get_forum(forum_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    forum = get_forum_by_id(forum_id)
    if not forum:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")
    return forum

# Eliminar un foro (solo el autor o admin)
@router.delete("/{forum_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_forum(forum_id: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    forum = get_forum_by_id(forum_id)
    if not forum:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")
    if user.role != "admin" and forum.id_user != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    deleted = delete_forum_by_id(forum_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete forum")
    return None
