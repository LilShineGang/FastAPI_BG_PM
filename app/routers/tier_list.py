
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.auth import decode_token, oauth2_scheme
from app.database import (
    delete_tier_list_by_id,
    get_all_tier_list,
    get_forum_by_id,
    get_tier_list_by_id,
    get_tier_lists_by_forum,
    insert_tier_list,
    update_tier_list_by_id,
)
from app.models import TierListIn, TierListOut

router = APIRouter(prefix="/tier-list", tags=["Tier List"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TierListOut)
async def create_tier_list(tier_list_in: TierListIn, token: str = Depends(oauth2_scheme)):
    decode_token(token)

    if tier_list_in.id_forum is not None:
        forum = get_forum_by_id(tier_list_in.id_forum)
        if not forum:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")
        existing = get_tier_lists_by_forum(tier_list_in.id_forum)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tier list already exists for this forum",
            )

    tier_list_id = insert_tier_list(tier_list_in)
    return TierListOut(
        id_tl=tier_list_id,
        name=tier_list_in.name,
        category=tier_list_in.category,
        description=tier_list_in.description,
        id_forum=tier_list_in.id_forum,
    )


@router.get("/", response_model=list[TierListOut], status_code=status.HTTP_200_OK)
async def read_all_tier_lists(token: str = Depends(oauth2_scheme)):
    decode_token(token)
    return get_all_tier_list() or []


@router.get("/{tier_list_id}/", response_model=TierListOut, status_code=status.HTTP_200_OK)
async def read_tier_list(tier_list_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    tier_list = get_tier_list_by_id(tier_list_id)
    if not tier_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tier list not found")
    return tier_list


@router.get("/forum/{forum_id}/", response_model=list[TierListOut], status_code=status.HTTP_200_OK)
async def read_tier_lists_by_forum(forum_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    return get_tier_lists_by_forum(forum_id) or []


@router.put("/{tier_list_id}/", response_model=TierListOut, status_code=status.HTTP_200_OK)
async def update_tier_list(
    tier_list_id: int, tier_list_in: TierListIn, token: str = Depends(oauth2_scheme)
):
    decode_token(token)
    existing = get_tier_list_by_id(tier_list_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tier list not found")

    if tier_list_in.id_forum is not None:
        forum = get_forum_by_id(tier_list_in.id_forum)
        if not forum:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")
        forum_lists = get_tier_lists_by_forum(tier_list_in.id_forum)
        if any(tl.id_tl != tier_list_id for tl in forum_lists):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tier list already exists for this forum",
            )

    updated = update_tier_list_by_id(tier_list_id, tier_list_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tier list could not be updated",
        )

    return TierListOut(
        id_tl=tier_list_id,
        name=tier_list_in.name,
        category=tier_list_in.category,
        description=tier_list_in.description,
        id_forum=tier_list_in.id_forum,
    )


@router.delete("/{tier_list_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tier_list(tier_list_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    deleted = delete_tier_list_by_id(tier_list_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tier list not found")
    return None
