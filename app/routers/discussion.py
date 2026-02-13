from fastapi import APIRouter, status, Depends, HTTPException
from app.models import DiscussionIn, DiscussionOut
from app.database import (
    insert_discussion,
    get_discussion_by_id,
    get_all_discussions,
    get_discussions_by_forum,
    update_discussion,
    delete_discussion,
    get_user_by_username,
)
from app.auth.auth import oauth2_scheme, decode_token, TokenData

router = APIRouter(
    prefix="/discussions",
    tags=["Discussions"]
)

# Crear una nueva discusion
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DiscussionOut)
async def create_discussion(discussion_in: DiscussionIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    discussion_id = insert_discussion(discussion_in, user.id)
    return DiscussionOut(id_discussion=discussion_id, name=discussion_in.name, comments=discussion_in.comments, posts=discussion_in.posts, rating=discussion_in.rating, id_forum=discussion_in.id_forum, id_user=user.id)

# Obtener todas las discusiones
@router.get("/", response_model=list[DiscussionOut])
async def get_all_discussions_endpoint(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    discussions = get_all_discussions()
    return [DiscussionOut(id_discussion=d.id_discussion, name=d.name, comments=d.comments, posts=d.posts, rating=d.rating, id_forum=d.id_forum, id_user=d.id_user) for d in discussions]

# Obtener una discusion por su id
@router.get("/{id_discussion}/", response_model=DiscussionOut)
async def get_discussion(id_discussion: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    discussion = get_discussion_by_id(id_discussion)
    if not discussion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")
    return DiscussionOut(id_discussion=discussion.id_discussion, name=discussion.name, comments=discussion.comments, posts=discussion.posts, rating=discussion.rating, id_forum=discussion.id_forum, id_user=discussion.id_user)

# Obtener discusiones por foro
@router.get("/forum/{id_forum}/", response_model=list[DiscussionOut])
async def get_discussions_by_forum_endpoint(id_forum: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    discussions = get_discussions_by_forum(id_forum)
    return [DiscussionOut(id_discussion=d.id_discussion, name=d.name, comments=d.comments, posts=d.posts, rating=d.rating, id_forum=d.id_forum, id_user=d.id_user) for d in discussions]

# Actualizar una discusion
@router.put("/{id_discussion}/", response_model=DiscussionOut)
async def update_discussion_endpoint(id_discussion: int, discussion_in: DiscussionIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    existing = get_discussion_by_id(id_discussion)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")
    updated = update_discussion(id_discussion, discussion_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Discussion could not be updated")
    return DiscussionOut(id_discussion=id_discussion, name=discussion_in.name, comments=discussion_in.comments, posts=discussion_in.posts, rating=discussion_in.rating, id_forum=discussion_in.id_forum, id_user=existing.id_user)

# Eliminar una discusion
@router.delete("/{id_discussion}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_discussion_endpoint(id_discussion: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    deleted = delete_discussion(id_discussion)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discussion not found")
    return None
