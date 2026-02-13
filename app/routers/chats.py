from fastapi import APIRouter, status, Depends, HTTPException
from app.models import ChatIn, ChatOut
from app.database import (
    insert_chat,
    get_chat_by_id,
    get_chats_by_message_instance,
    get_all_chats,
    delete_chat,
    get_message_instance_by_id,
)
from app.auth.auth import oauth2_scheme, decode_token, TokenData

router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)

# Crear un nuevo chat (he tenido que hacerlo linkeado a messages_instances)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ChatOut)
async def create_chat(chat_in: ChatIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    # Verificar que existe el message_instance
    message = get_message_instance_by_id(chat_in.id_mi)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message instance not found")
    chat_id = insert_chat(chat_in)
    return ChatOut(id_chat=chat_id, id_mi=chat_in.id_mi, content=chat_in.content)

# Obtener todos los chats
@router.get("/", response_model=list[ChatOut])
async def get_all_chats_endpoint(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    chats = get_all_chats()
    return [ChatOut(id_chat=c.id_chat, id_mi=c.id_mi, content=c.content, timestamp=c.timestamp) for c in chats]

# Obtener un chat por su id
@router.get("/{id_chat}/", response_model=ChatOut)
async def get_chat(id_chat: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    chat = get_chat_by_id(id_chat)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return ChatOut(id_chat=chat.id_chat, id_mi=chat.id_mi, content=chat.content, timestamp=chat.timestamp)

# Obtener chats por message_instance
@router.get("/message/{id_mi}/", response_model=list[ChatOut])
async def get_chats_by_message(id_mi: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    chats = get_chats_by_message_instance(id_mi)
    return [ChatOut(id_chat=c.id_chat, id_mi=c.id_mi, content=c.content, timestamp=c.timestamp) for c in chats]

# Eliminar un chat
@router.delete("/{id_chat}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_endpoint(id_chat: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    deleted = delete_chat(id_chat)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return None
