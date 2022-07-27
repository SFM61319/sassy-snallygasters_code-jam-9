import websockets
# import asyncio
# from wild_chess.utils import board
from wild_chess.setup import setup


class Server:
    """
    The server class.
    """

    db_con: setup.Setup

    @staticmethod
    async def handler(websocket: websockets.WebSocketServerProtocol) -> None:
        """
        Handle a new connection.
        """
        data = await websocket.recv()
        reply = f"Data received: {data}"
        print(reply)
        await websocket.send(reply)

    async def setup(self) -> None:
        """
        Start the server.
        """
        self.db_con = setup.Setup()
        await self.db_con.setup()

    async def start(self) -> None:
        """
        Start the server.
        """
        await self.setup()
        start_server = websockets.serve(self.handler, "localhost", 8000)
        await start_server

    async def stop(self) -> None:
        """
        Stop the server.
        """
        await self.db_con.pool.close()
