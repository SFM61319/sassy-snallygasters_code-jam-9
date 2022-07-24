import asyncio
import os

import asyncpg

from wild_chess.database import PlayerDB


class Setup:  # setup class
    """
    Class methods for setup.
    """

    pool: asyncpg.pool.Pool  # asyncpg pool
    db: PlayerDB  # database

    async def set_db(self) -> None:  # connect to database
        """ "
        Set the database.
        Uses asyncpg to connect to the database.
        Fetches keys from the environment.
        """
        self.pool = await asyncpg.create_pool(
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT"),
            database=os.getenv("PGDATABASE"),
            ssl="require",
            loop=asyncio.get_event_loop(),
        )

    async def setup(self) -> None:  # setup to set all connections
        await self.set_db()
        self.db = PlayerDB()
        await self.db.set_table(self.pool)
