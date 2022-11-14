from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from django.http import JsonResponse

import requests

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login2():
    response = requests.get("https://launchpad.37signals.com/authorization/token")
    print(response)
    return "response"
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def users():
    # # Get a copy of the default headers that requests would use
    # headers = requests.utils.default_headers()

    # # Update the headers with your custom ones
    # # You don't have to worry about case-sensitivity with
    # # the dictionary keys, because default_headers uses a custom
    # # CaseInsensitiveDict implementation within requests' source code.
    # headers.update(
    #     {
    #         'User-Agent': 'My User Agent 1.0',
    #     }
    # )
    response = requests.get("https://launchpad.37signals.com/authorization/new?type=web_server&client_id=fdfcd31459e0e7491296ea11a0dd53ab984e3417&client_secret=3be318f63a3047d55fcb84d22959a6c6f77e62f2&redirect_uri=http://localhost:8000/token")
    print(JsonResponse(response))
    return "response"
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
