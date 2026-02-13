from fastapi import APIRouter, status, Depends, HTTPException
from app.models import BuildIn, BuildOut
from app.database import (
    insert_build,
    get_build_by_id,
    get_all_builds,
    get_builds_by_forum,
    update_build,
    delete_build,
    get_user_by_username,
)
from app.auth.auth import oauth2_scheme, decode_token, TokenData

router = APIRouter(
    prefix="/builds",
    tags=["Builds"]
)

# Crear nueva build
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BuildOut)
async def create_build(build_in: BuildIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    build_id = insert_build(build_in)
    return BuildOut(id_build=build_id, name=build_in.name, planner=build_in.planner, category=build_in.category, description=build_in.description, id_forum=build_in.id_forum)

# Obtener todos los builds
@router.get("/", response_model=list[BuildOut])
async def get_all_builds(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    builds = get_all_builds()
    return [BuildOut(id_build=b.id_build, name=b.name, planner=b.planner, category=b.category, description=b.description, id_forum=b.id_forum) for b in builds]

# Obtener build por id
@router.get("/{id_build}/", response_model=BuildOut)
async def get_build(id_build: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    build = get_build_by_id(id_build)
    if not build:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Build not found")
    return BuildOut(id_build=build.id_build, name=build.name, planner=build.planner, category=build.category, description=build.description, id_forum=build.id_forum)

# Obtener builds por foro
@router.get("/forum/{id_forum}/", response_model=list[BuildOut])
async def get_builds_by_forum_endpoint(id_forum: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    builds = get_builds_by_forum(id_forum)
    return [BuildOut(id_build=b.id_build, name=b.name, planner=b.planner, category=b.category, description=b.description, id_forum=b.id_forum) for b in builds]

# Actualizar build
@router.put("/{id_build}/", response_model=BuildOut)
async def update_build_endpoint(id_build: int, build_in: BuildIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    existing = get_build_by_id(id_build)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Build not found")
    updated = update_build(id_build, build_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Build could not be updated")
    return BuildOut(id_build=id_build, name=build_in.name, planner=build_in.planner, category=build_in.category, description=build_in.description, id_forum=build_in.id_forum)

# Eliminar build
@router.delete("/{id_build}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_build_endpoint(id_build: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    deleted = delete_build(id_build)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Build not found")
    return None
