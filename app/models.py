from pydantic import BaseModel

class UserBase(BaseModel):
    username:str
    password:str

class UserIn(UserBase):
    name:str
    email:str
    image:str | None = None

class UserDb(UserIn):
    id:int

class UserOut(BaseModel):
    id:int
    name:str
    username:str
    email:str
    image:str | None = None

#class UserLoginIn(UserBase):
#    pass
    
class TokenOut(BaseModel):
    token:str
