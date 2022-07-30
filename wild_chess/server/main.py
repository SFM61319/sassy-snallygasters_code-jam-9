"""main server file"""

import fastapi
import uvicorn

from wild_chess.server.routes import authentication
from wild_chess.server.routes import leaderboard
from wild_chess.server.routes import multiplayer

app = fastapi.FastAPI()

app.include_router(authentication.route)
app.include_router(leaderboard.route)
app.include_router(multiplayer.route)


def main() -> None:
    """Driver code."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
