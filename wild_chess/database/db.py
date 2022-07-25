from __future__ import annotations

from typing import List, Optional, Tuple

import asyncpg

from ..utils import PlayerRecord
from .postgres import DatabaseModel

__all__: Tuple[str, ...] = ("PlayerDB",)


class PlayerDB(DatabaseModel):  # subclass of DatabaseModel for player data
    """
    all abstract methods for using player database.
    """

    pool: asyncpg.pool.Pool

    async def set_table(self, pool: asyncpg.pool.Pool) -> None:
        """
        Set the database connection pool. And create the table if it doesn't exist.
        :param pool:
        :return:
        """
        self.pool = pool
        await self.exec_write_query(
            """CREATE TABLE IF NOT EXISTS players(
                                       name TEXT PRIMARY KEY,
                                       wins BIGINT,
                                       losses BIGINT,
                                       ties BIGINT,
                                       history TEXT[])"""
        )

    async def drop_table(self) -> None:
        """
        Drop the table.
        :return:
        """
        await self.exec_write_query("DROP TABLE players")

    async def find_player(self, user_name: str) -> Optional[PlayerRecord]:
        """
        Find a player by name.
        :param user_name:
        :return:
        """
        record = await self.exec_fetchone("SELECT * FROM players WHERE name = $1", (user_name,))
        return PlayerRecord(*record) if record else None

    async def create_player(self, user_name: str) -> Optional[PlayerRecord] | bool:
        """
        Create a new player.
        :param user_name:
        :return:
        """
        player = await self.find_player(user_name)
        if player is not None:
            return False
        await self.exec_write_query(
            "INSERT INTO players VALUES ($1, 0, 0, 0, $2)",
            (
                user_name,
                [],
            ),
        )
        return await self.find_player(user_name)

    async def remove_player(self, user_name: str) -> bool:
        """
        Remove a player.
        :param user_name:
        :return:
        """
        player = await self.find_player(user_name)
        if player is None:
            return False
        await self.exec_write_query("DELETE FROM players WHERE name = $1", (user_name,))
        return True

    async def update_player_win(self, user_name: str) -> bool:
        """
        Update a player's win.
        :param user_name:
        :return:
        """
        player = await self.find_player(user_name)
        if player is None:
            return False
        await self.exec_write_query("UPDATE players SET wins = wins + 1 WHERE name = $1", (user_name,))
        return True

    async def update_player_loss(self, user_name: str) -> bool:
        """
        Update a player's loss.
        :param user_name:
        :return:
        """
        player = await self.find_player(user_name)
        if player is None:
            return False
        await self.exec_write_query("UPDATE players SET losses = losses + 1 WHERE name = $1", (user_name,))
        return True

    async def update_player_tie(self, user_name: str) -> bool:
        """
        Update a player's tie.
        :param user_name:
        :return:
        """
        player = await self.find_player(user_name)
        if player is None:
            return False
        await self.exec_write_query("UPDATE players SET ties = ties + 1 WHERE name = $1", (user_name,))
        return True

    async def update_player_history(self, user_name: str, player_name: str, moves: list, status: str) -> bool:
        """
        Update a player's history.
        :param user_name:
        :param player_name:
        :param moves:
        :param status:
        :return:
        """
        player = await self.find_player(user_name)
        if player is None:
            return False
        history = player.history
        container = {"opponent": player_name, "moves": moves, "status": status}
        history.append(str(container))
        await self.exec_write_query("UPDATE players SET history = $1 WHERE name = $2", (history, user_name))
        return True

    async def all_players(self) -> List[PlayerRecord]:
        """
        Get all players.
        :return:
        """
        records = await self.exec_fetchall("SELECT * FROM players")
        return [PlayerRecord(*record) for record in records]
