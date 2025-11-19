from pydantic import basemodel 

class UserBase(BaseModel):
    nickname:str
    password:str

class UserIn(UserBase):
    name:str

class UserDb(UserIn):
    id:int

class UserLogin(UserBase):
    pass
    
class TokenOut(BaseModel):
    token:str
