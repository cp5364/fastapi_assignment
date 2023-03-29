from pydantic import BaseModel


class PostAddress(BaseModel):
    """ Request body format for address along with co-ordinate data"""
    user_id:int
    full_address:str

    class Config():
        orm_mode = True


class UpdateAddress(BaseModel):
    """ Request body format for address along with co-ordinate data"""
    full_address:str

    class Config():
        orm_mode = True


class User(BaseModel):
    """ Request body format for user details"""
    name:str
    email:str
    password:str

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True
