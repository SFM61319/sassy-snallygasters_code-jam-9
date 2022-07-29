"""contains authentication functions"""


import fastapi

from wild_chess.database import db

route = fastapi.APIRouter()


@route.post("/signup")
async def signup(username: str, password: str) -> dict:
    """
    Signs a user up.

    :param username:
    :param password:
    :return:
    """
    player = await db.PlayerDB().create_player(username, password)
    return {"message": "user_created"} if player else {"message": "username already exists"}


@route.post("/login")
async def login(username: str, password: str) -> dict:
    """
    Logs the user in.

    :param username:
    :param password:
    :return:
    """
    player = await db.PlayerDB().check_password(username, password)
    return {"message": "login_successful"} if player else {"message": "login_failed"}
