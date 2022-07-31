"""contains authentication functions"""


import fastapi

from ...setup.setup import Setup
route = fastapi.APIRouter()


@route.post("/signup")
async def signup(username: str, password: str) -> dict:
    """
    Signs a user up.

    :param username:
    :param password:
    :return:
    """
    setup = Setup()
    await setup.setup()
    player = await setup.database.create_player(username, password)
    await setup.close()
    return {"message": "user_created"} if player else {"message": "username already exists"}


@route.post("/login")
async def login(username: str, password: str) -> dict:
    """
    Logs the user in.

    :param username:
    :param password:
    :return:
    """
    setup = Setup()
    await setup.setup()
    player = await setup.database.check_password(username, password)
    await setup.close()
    return {"message": "login_successful"} if player else {"message": "login_failed"}
