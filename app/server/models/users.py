from typing import Union,List
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None    
    class Config:
        schema_extra = {
            "example": {
                "username": "JohnDoe",
                "password": "XXXXXX",
                "email": "John@gmail.com",
                "full_name": "your fullname",
                "disabled": "true or false",
            }
        }
        

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}