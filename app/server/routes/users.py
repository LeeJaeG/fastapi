from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status,Security
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from typing import List, Union

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from server.database import (
    add_user,
    retrieve_user,
    retrieve_users,
)
from server.models.users import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    Token,
    TokenData,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="user/token",
    scopes={"me": "Read information about the current user.", "items": "Read items.","action": "Read"},
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Item(BaseModel):
    username: str
    password: str
    scopes: str ="me"


router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await retrieve_user(username)
    print(user)
    if not user:
        return False
    print(password)
    if not verify_password(password, user['password']):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await retrieve_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: UserSchema = Security(get_current_user, scopes=["me"])):
    print(1)
    print(current_user['disabled'])
    print(2)
    if current_user['disabled']:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/", response_description="user data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    
    user.password=pwd_context.hash(user.password)
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "user added successfully.")

@router.get("/", response_description="users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="user data retrieved")
async def get_user_data(username):
    user = await retrieve_user(username)
    if user:
        return ResponseModel(user, "user data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "user doesn't exist.")



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Item):
    user = await authenticate_user( form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "scopes": form_data.scopes}, expires_delta=access_token_expires
    )
    print({"access_token": access_token, "token_type": "bearer"})
    json = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
    print(json)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me/items/")
async def read_own_items(
    current_user: UserSchema = Security(get_current_active_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user['username']}]


@router.get("/status/")
async def read_system_status(current_user: UserSchema = Depends(get_current_user)):
    return {"status": "ok"}