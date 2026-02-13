from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.auth import decode_token, oauth2_scheme
from app.database import (
    delete_achievement_by_id,
    get_achievement_by_id,
    get_achievements_by_game,
    get_all_achievements,
    get_game_by_id,
    insert_achievement,
    update_achievement_by_id,
)
from app.models import AchievementIn, AchievementOut

router = APIRouter(prefix="/achievements", tags=["Achievements"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AchievementOut)
async def create_achievement(
    achievement_in: AchievementIn, token: str = Depends(oauth2_scheme)
):
    decode_token(token)
    if achievement_in.id_game is not None:
        game = get_game_by_id(achievement_in.id_game)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    achievement_id = insert_achievement(achievement_in)
    return AchievementOut(
        id_achievement=achievement_id,
        difficulty=achievement_in.difficulty,
        description=achievement_in.description,
        id_game=achievement_in.id_game,
    )


@router.get("/", response_model=list[AchievementOut], status_code=status.HTTP_200_OK)
async def read_all_achievements(token: str = Depends(oauth2_scheme)):
    decode_token(token)
    return get_all_achievements() or []


@router.get("/{achievement_id}/", response_model=AchievementOut, status_code=status.HTTP_200_OK)
async def read_achievement(achievement_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    achievement = get_achievement_by_id(achievement_id)
    if not achievement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")
    return achievement


@router.get(
    "/game/{game_id}/",
    response_model=list[AchievementOut],
    status_code=status.HTTP_200_OK,
)
async def read_achievements_by_game(game_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    return get_achievements_by_game(game_id) or []


@router.put("/{achievement_id}/", response_model=AchievementOut, status_code=status.HTTP_200_OK)
async def update_achievement(
    achievement_id: int, achievement_in: AchievementIn, token: str = Depends(oauth2_scheme)
):
    decode_token(token)
    existing = get_achievement_by_id(achievement_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")

    if achievement_in.id_game is not None:
        game = get_game_by_id(achievement_in.id_game)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    updated = update_achievement_by_id(achievement_id, achievement_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Achievement could not be updated"
        )

    return AchievementOut(
        id_achievement=achievement_id,
        difficulty=achievement_in.difficulty,
        description=achievement_in.description,
        id_game=achievement_in.id_game,
    )


@router.delete("/{achievement_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_achievement(achievement_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token)
    deleted = delete_achievement_by_id(achievement_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")
    return None
