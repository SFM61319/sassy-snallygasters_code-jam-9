"""main server file"""

import uvicorn
from fastapi import FastAPI

from wild_chess.server.routes.authentication import route as authentication_router
from wild_chess.server.routes.leaderboard import route as leaderboard_router

app = FastAPI()

app.include_router(authentication_router)
app.include_router(leaderboard_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
