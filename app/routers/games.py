# games router

from app.models import GameIn, GameOut, GameDb
from fastapi import APIRouter, status, HTTPException, Depends
from app.database import insert_game, get_game_by_name, get_all_games, delete_game_by_name
from app.auth.auth import oauth2_scheme, decode_token, TokenData
from app.database import get_user_by_username


router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GameOut)
async def create_game(game_in: GameIn, token: str = Depends(oauth2_scheme)):
    # Verificar autenticación
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    # Verificar si el juego ya existe
    existing_game = get_game_by_name(game_in.name)
    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Game already exists"
        )
    
    # Insertar juego en la base de datos
    game_id = insert_game(
        GameDb(
            id_game=0, 
            name=game_in.name,
            gender=game_in.gender,
            difficulty=game_in.difficulty,
            rating=game_in.rating,
            image=game_in.image,
            category=game_in.category
        )
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


@router.get("/", response_model=list[GameOut], status_code=status.HTTP_200_OK)
async def get_games(token: str = Depends(oauth2_scheme)):
    # Verificar autenticación
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    # Obtener todos los juegos de la base de datos
    all_games = get_all_games()
    return [
        GameOut(
            id_game=gameDb.id_game,
            name=gameDb.name,
            gender=gameDb.gender,
            difficulty=gameDb.difficulty,
            rating=gameDb.rating,
            image=gameDb.image,
            category=gameDb.category
        )
        for gameDb in all_games
    ]


@router.get("/{name}/", response_model=GameOut)
async def read_game(name: str, token: str = Depends(oauth2_scheme)):
    # Verificar autenticación
    decode_token(token)
    
    game_found = get_game_by_name(name)
    
    if game_found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game {name} not found"
        )
    
    return GameOut(
        id_game=game_found.id_game,
        name=game_found.name,
        gender=game_found.gender,
        difficulty=game_found.difficulty,
        rating=game_found.rating,
        image=game_found.image,
        category=game_found.category
    )


# Borrar juego
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(name: str, token: str = Depends(oauth2_scheme)):
    # Verificar autenticación
    decode_token(token)

    game_found = get_game_by_name(name)
    
    if game_found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Eliminar juego de la base de datos
    deleted = delete_game_by_name(name)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete game"
        )
    
    return None  # 204
