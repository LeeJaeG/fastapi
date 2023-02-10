from typing import Optional
from typing import Union
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "username": "John Doe",
                "password": "XXXXXX",
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Union[str, None] = None

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}