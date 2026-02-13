from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.auth import TokenData, decode_token, oauth2_scheme
from app.database import (
    delete_group_by_id,
    get_all_groups,
    get_forum_by_id,
    get_group_by_id,
    get_groups_by_forum,
    get_user_by_username,
    insert_group,
    update_group_by_id,
)
from app.models import GroupIn, GroupOut

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GroupOut)
async def create_group(group_in: GroupIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if group_in.id_forum is not None:
        forum = get_forum_by_id(group_in.id_forum)
        if not forum:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")

    group_id = insert_group(group_in, user.id)
    return GroupOut(
        id_group=group_id,
        name=group_in.name,
        admin=user.id,
        description=group_in.description,
        image=group_in.image,
        id_forum=group_in.id_forum,
    )


@router.get("/", response_model=list[GroupOut], status_code=status.HTTP_200_OK)
async def read_all_groups(token: str = Depends(oauth2_scheme)):
    decode_token(token)
    return get_all_groups() or []


@router.get("/{group_id}/", response_model=GroupOut, status_code=status.HTTP_200_OK)
async def read_group(group_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    group = get_group_by_id(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group


@router.get("/forum/{forum_id}/", response_model=list[GroupOut], status_code=status.HTTP_200_OK)
async def read_groups_by_forum(forum_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    return get_groups_by_forum(forum_id) or []


@router.put("/{group_id}/", response_model=GroupOut, status_code=status.HTTP_200_OK)
async def update_group(group_id: int, group_in: GroupIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    existing = get_group_by_id(group_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user.role != "admin" and existing.admin != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    if group_in.id_forum is not None:
        forum = get_forum_by_id(group_in.id_forum)
        if not forum:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")

    updated = update_group_by_id(group_id, group_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group could not be updated",
        )

    return GroupOut(
        id_group=group_id,
        name=group_in.name,
        admin=existing.admin,
        description=group_in.description,
        image=group_in.image,
        id_forum=group_in.id_forum,
    )


@router.delete("/{group_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    group = get_group_by_id(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user.role != "admin" and group.admin != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    deleted = delete_group_by_id(group_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete group",
        )
    return None
