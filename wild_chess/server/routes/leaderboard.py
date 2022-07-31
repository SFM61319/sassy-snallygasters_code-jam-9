"""Leaderboard function"""


import fastapi

from ...setup.setup import Setup
from wild_chess.utils import data

route = fastapi.APIRouter()


@route.get("/leaderboard")
async def get_leaderboard() -> dict[str, list[data.PlayerRecord]]:
    """Gets the leaderboard data"""
    setup = Setup()
    await setup.setup()
    board = await setup.database.leaderboard()
    await setup.close()
    return {"leaderboard": board}
