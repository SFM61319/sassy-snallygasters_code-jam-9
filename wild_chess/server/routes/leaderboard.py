"""leaderboard function"""

from fastapi import APIRouter

from wild_chess.database.db import PlayerDB

route = APIRouter()


@route.get("/leaderboard")
async def get_leaderboard() -> dict:
    """Gets the leaderboard data"""
    board = await PlayerDB().leaderboard()
    return {"leaderboard": board}
