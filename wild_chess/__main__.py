"""Main file."""

import asyncio
from wild_chess.server import server


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(server.Server().start())
    asyncio.get_event_loop().run_forever()
