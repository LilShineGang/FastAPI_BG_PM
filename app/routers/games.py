from fastapi import APIRouter, status, Depends, HTTPException
from app.models import GameIn, GameOut
from app.database import get_all_game, get_user_by_username, insert_game, get_game_by_name
from app.auth.auth import oauth2_scheme, decode_token, TokenData

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)



# Endpoint para crear un nuevo juego 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GameOut)
async def create_game(game_in: GameIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)

    existing_game = get_game_by_name(game_in.name)
    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Game with this name already exists"
        )

    game_id = insert_game(game_in)


    return GameOut(id_game=game_id, name=game_in.name, gender=game_in.gender, difficulty=game_in.difficulty, rating=game_in.rating, image=game_in.image, category=game_in.category)


from fastapi import Query
@router.get("/search/", response_model=GameOut)
async def read_game(name: str = Query(..., description="Nombre del juego"), token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)

    game = get_game_by_name(name)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game '{name}' not found"
        )

    return GameOut(
        id_game=game.id_game,
        name=game.name,
        gender=game.gender,
        difficulty=game.difficulty,
        rating=game.rating,
        image=game.image,
        category=game.category
    )


@router.get("/", response_model=list[GameOut], status_code=status.HTTP_200_OK)
async def read_all_games(token: str = Depends(oauth2_scheme)):
    # Verificamos token
    data: TokenData = decode_token(token)

    if not data.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    all_games = get_all_game() or []
    return [
        GameOut(
            id_game=db_game.id_game,
            name=db_game.name,
            gender=db_game.gender,
            difficulty=db_game.difficulty,
            rating=db_game.rating,
            image=db_game.image,
            category=db_game.category
        )
        for db_game in all_games
    ]

@router.put("/{id}/", response_model=GameOut, status_code=status.HTTP_200_OK)
async def update_game(game_id: int, game_in: GameIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    from app.database import update_game_by_id, get_game_by_name
    # Verificar si el juego existe
    existing_game = get_game_by_name(game_in.name)
    if not existing_game or existing_game.id_game != game_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    # Actualizar el juego
    updated = update_game_by_id(game_id, game_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game could not be updated"
        )
    return GameOut(
        id_game=game_id,
        name=game_in.name,
        gender=game_in.gender,
        difficulty=game_in.difficulty,
        rating=game_in.rating,
        image=game_in.image,
        category=game_in.category
    )

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    from app.database import delete_game_by_id
    deleted = delete_game_by_id(game_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return None
