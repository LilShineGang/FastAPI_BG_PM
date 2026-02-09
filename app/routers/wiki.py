from fastapi import APIRouter, status, Depends, HTTPException
from app.models import WikiIn, WikiOut
from app.database import (
    insert_wiki,
    get_wiki_by_id,
    get_all_wiki,
    get_wikis_by_forum,
    update_wiki_by_id,
    delete_wiki_by_id,
    get_forum_by_id,
)
from app.auth.auth import oauth2_scheme, decode_token

router = APIRouter(
    prefix="/wiki",
    tags=["Wiki"]
)


# Crear una wiki
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WikiOut)
async def create_wiki(wiki_in: WikiIn, token: str = Depends(oauth2_scheme)):
    decode_token(token)

    if wiki_in.id_forum is not None:
        forum = get_forum_by_id(wiki_in.id_forum)
        if not forum:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")

    wiki_id = insert_wiki(wiki_in)
    return WikiOut(
        id_wiki=wiki_id,
        name=wiki_in.name,
        category=wiki_in.category,
        description=wiki_in.description,
        id_forum=wiki_in.id_forum
    )


# Obtener todas las wikis
@router.get("/", response_model=list[WikiOut], status_code=status.HTTP_200_OK)
async def read_all_wiki(token: str = Depends(oauth2_scheme)):
    decode_token(token)
    return get_all_wiki() or []


# Obtener wiki por id
@router.get("/{wiki_id}/", response_model=WikiOut, status_code=status.HTTP_200_OK)
async def read_wiki(wiki_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    wiki = get_wiki_by_id(wiki_id)
    if not wiki:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wiki not found")
    return wiki


# Obtener wikis por foro
@router.get("/forum/{forum_id}/", response_model=list[WikiOut], status_code=status.HTTP_200_OK)
async def read_wikis_by_forum(forum_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    return get_wikis_by_forum(forum_id) or []


# Actualizar wiki
@router.put("/{wiki_id}/", response_model=WikiOut, status_code=status.HTTP_200_OK)
async def update_wiki(wiki_id: int, wiki_in: WikiIn, token: str = Depends(oauth2_scheme)):
    decode_token(token)

    existing = get_wiki_by_id(wiki_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wiki not found")

    if wiki_in.id_forum is not None:
        forum = get_forum_by_id(wiki_in.id_forum)
        if not forum:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")

    updated = update_wiki_by_id(wiki_id, wiki_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wiki could not be updated")

    return WikiOut(
        id_wiki=wiki_id,
        name=wiki_in.name,
        category=wiki_in.category,
        description=wiki_in.description,
        id_forum=wiki_in.id_forum
    )


# Eliminar wiki
@router.delete("/{wiki_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wiki(wiki_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    deleted = delete_wiki_by_id(wiki_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wiki not found")
    return None
