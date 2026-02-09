# post (para crear una guia), un get de game para el id del foro, un get de guia y un delete de guia.
from fastapi import APIRouter, Depends, HTTPException, status  # pyright: ignore[reportMissingImports]

from app.auth.auth import TokenData, decode_token, oauth2_scheme
from app.database import (
    delete_guide_by_id,
    get_guide_by_id,
    get_user_by_username,
    insert_guide,
)
from app.database import (
    get_guides_by_forum as db_get_guides_by_forum,
)
from app.models import GuideIn, GuideOut

router = APIRouter(prefix="/guides", tags=["Guides"])


# Creamos una nueva guia
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GuideOut)
async def create_guide(guide_in: GuideIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    forum = db_get_guides_by_forum(guide_in.forum_id)
    if not forum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found"
        )
    guide_id = insert_guide(guide_in, user.id, forum.id_forum)
    return GuideOut(
        id_guide=guide_id,
        name=guide_in.name,
        difficulty=guide_in.difficulty,
        category=guide_in.category,
    )


# Obtener una guia por su id
@router.get("/{guide_id}/", response_model=GuideOut)
async def get_guide(guide_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    guide = get_guide_by_id(guide_id)
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guide not found"
        )
    return guide


# Para eliminar una guia
@router.delete("/{guide_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guide(guide_id: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    guide = get_guide_by_id(guide_id)
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guide not found"
        )
    if guide.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    deleted = delete_guide_by_id(guide_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete guide",
        )
    return None


# Para obtener todas las guias que pertenecen a un foro
@router.get("/forum/{forum_id}/", response_model=list[GuideOut])
async def get_guides_by_forum(forum_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    guides = db_get_guides_by_forum(forum_id)
    if not guides:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guides not found"
        )
    return guides
