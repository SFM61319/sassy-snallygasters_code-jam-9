"""Leaderboard function"""


import fastapi

from wild_chess.server.routes.db_setup import db
from wild_chess.utils import data

route = fastapi.APIRouter()


@route.get("/leaderboard")
async def get_leaderboard() -> dict[str, list[data.PlayerRecord]]:
    """Gets the leaderboard data"""
    board = await db.database.leaderboard()
    return {"leaderboard": board}
