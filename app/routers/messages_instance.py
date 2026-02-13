from fastapi import APIRouter, status, Depends, HTTPException
from app.models import MessageInstanceIn, MessageInstanceOut
from app.database import (
    insert_message_instance,
    get_message_instance_by_id,
    get_all_messages_instance,
    delete_message_instance,
)
from app.auth.auth import oauth2_scheme, decode_token, TokenData

router = APIRouter(
    prefix="/messages-instance",
    tags=["MessagesInstance"]
)

# Crear un nuevo mensaje instancia
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MessageInstanceOut)
async def create_message_instance(message_in: MessageInstanceIn, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    message_id = insert_message_instance(message_in)
    return MessageInstanceOut(id_mi=message_id, status=message_in.status, content=message_in.content)

# Obtener todos los mensajes instancia
@router.get("/", response_model=list[MessageInstanceOut])
async def get_all_messages(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    messages = get_all_messages_instance()
    return [MessageInstanceOut(id_mi=m.id_mi, status=m.status, content=m.content, timestamp=m.timestamp) for m in messages]

# Obtener un mensaje instancia por su id
@router.get("/{id_mi}/", response_model=MessageInstanceOut)
async def get_message_instance(id_mi: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    message = get_message_instance_by_id(id_mi)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return MessageInstanceOut(id_mi=message.id_mi, status=message.status, content=message.content, timestamp=message.timestamp)

# Eliminar un mensaje instancia
@router.delete("/{id_mi}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message_instance_endpoint(id_mi: int, token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    deleted = delete_message_instance(id_mi)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return None
