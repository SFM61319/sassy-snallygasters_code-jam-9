"""contains authentication functions"""

from fastapi import APIRouter

from wild_chess.database.db import PlayerDB

route = APIRouter()


@route.post("/create_user")
async def create_user(username: str, password: str) -> dict:
    """
    Creates user

    :param username:
    :param password:
    :return:
    """
    player = await PlayerDB().create_player(username, password)
    return {"message": "user_created"} if player else {"message": "username already exists"}


@route.post("/login")
async def login(username: str, password: str) -> dict:
    """
    For login

    :param username:
    :param password:
    :return:
    """
    player = await PlayerDB().check_password(username, password)
    return {"message": "login_successful"} if player else {"message": "login_failed"}
