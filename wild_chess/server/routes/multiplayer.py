"""multiplayer functions"""


import random

import fastapi

route = fastapi.APIRouter()
active_game: dict = {}


@route.post("/host-game")
async def host_game(username: str) -> dict[str, list[str]]:
    """
    Hosts the game.

    :param username:
    :type username: str
    :return:
    :rtype: dict[str, list[str]]
    """
    code = ['0', '1', '2', '3', '4', '5']

    random.shuffle(code)
    shuffled = "".join(code)

    active_game[username] = {"code": shuffled, "board": None, "players": [username]}
    return {"code": code}


@route.post("/join-game/{code}")
async def join_game(code: str, username: str) -> dict[str, str]:
    """
    Joins the game.

    :param code:
    :type code: str
    :param username:
    :type username: str
    :return:
    :rtype: dict[str, str]
    """
    for v in active_game.values():
        if v["code"] == code:
            if len(v["players"]) == 1 and username not in v["players"]:
                v["players"].append(username)
                return {"message": "ok"}

    return {"message": "error"}


@route.post("/game/{code}")
async def post_game(code: str, username: str, board: list[list[str]]) -> dict[str, str]:
    """
    Posts the game.

    :param code:
    :type code: str
    :param username:
    :type username: str
    :param board:
    :type board: list[list[str]]
    :return:
    :rtype: dict[str, str]
    """
    for v in active_game.values():
        if v["code"] == code and username in v["players"]:
            v["board"] = board
            return {"message": "ok"}

    return {"message": "error"}


@route.get("/game/{code}")
async def get_board(code: str, username: str) -> dict[str, str | list[list[str]]]:
    """
    Gets the board.

    :param code:
    :type code: str
    :param username:
    :type username: str
    :return:
    :rtype: dict[str, str | list[list[str]]]
    """
    for v in active_game.values():
        if v["code"] == code and username in v["players"]:
            return {"board": v["board"]}

    return {"board": "error"}
