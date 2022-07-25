"""Database module."""


from __future__ import annotations
import typing

import asyncpg

from wild_chess.utils import data
from wild_chess.database import postgres


__all__: tuple[str, ...] = ("PlayerDB",)


class PlayerDB(postgres.DatabaseModel):
    """All abstract methods for using player database."""

    pool: asyncpg.pool.Pool

    async def set_table(self, pool: asyncpg.pool.Pool) -> None:
        """
        Set the database connection pool. And create the table if it doesn't exist.

        :param pool:
        :type pool: asyncpg.pool.Pool
        """
        self.pool = pool

        # TODO: Use a better primary key field
        await self.exec_write_query(
            """CREATE TABLE IF NOT EXISTS players(
                                       name TEXT PRIMARY KEY,
                                       wins BIGINT,
                                       losses BIGINT,
                                       ties BIGINT,
                                       history TEXT[])"""
        )

    async def drop_table(self) -> None:
        """Drop the table."""
        await self.exec_write_query("DROP TABLE players")

    async def find_player(self, username: str) -> typing.Optional[data.PlayerRecord]:
        """
        Find a player by name.

        :param username:
        :type username: str
        :return:
        :rtype: typing.Optional[data.PlayerRecord]
        """
        record = await self.exec_fetchone("SELECT * FROM players WHERE name = $1", (username,))
        return data.PlayerRecord(*record) if record else None

    async def create_player(self, username: str) -> typing.Optional[data.PlayerRecord] | bool:
        """
        Create a new player.

        :param username:
        :type username: str
        :return:
        :rtype: typing.Optional[data.PlayerRecord] | bool
        """
        player = await self.find_player(username)

        if player is not None:
            return False

        await self.exec_write_query(
            "INSERT INTO players VALUES ($1, 0, 0, 0, $2)",
            (
                username,
                [],
            ),
        )
        return await self.find_player(username)

    async def try_exec_write_query(self, username: str, query: str, query_data: typing.Optional[tuple] = None) -> bool:
        """
        Tries to execute a write query. Returns True if player with *username* exists, False otherwise.

        :param username: The username of the player
        :type username: str
        :param query: The write query to execute
        :type query: str
        :param query_data: The variables to replace in the query (if any), defaults to None
        :type query_data: typing.Optional[tuple], optional
        :return: True if player exists, False otherwise.
        :rtype: bool
        """
        player = await self.find_player(username)

        if player is None:
            return False

        await self.exec_write_query(query, query_data)
        return True

    async def remove_player(self, username: str) -> bool:
        """
        Remove a player.

        :param username:
        :type username:
        :return:
        :rtype: bool
        """
        return await self.try_exec_write_query(username, "DELETE FROM players WHERE name = $1", (username,))

    async def update_player_win(self, username: str) -> bool:
        """
        Update a player's win.

        :param username:
        :type username: str
        :return:
        :rtype: bool
        """
        return await self.try_exec_write_query(username, "UPDATE players SET wins = wins + 1 WHERE name = $1", (username,))

    async def update_player_loss(self, username: str) -> bool:
        """
        Update a player's loss.

        :param username:
        :type username: str
        :return:
        :rtype: bool
        """
        return await self.try_exec_write_query(username, "UPDATE players SET losses = losses + 1 WHERE name = $1", (username,))

    async def update_player_tie(self, username: str) -> bool:
        """
        Update a player's tie.

        :param username:
        :type username: str
        :return:
        :rtype bool:
        """
        return await self.try_exec_write_query(username, "UPDATE players SET ties = ties + 1 WHERE name = $1", (username,))

    async def update_player_history(self, username: str, player_name: str, moves: list, status: str) -> bool:
        """
        Update a player's history.

        :param username:
        :type username: str
        :param player_name:
        :type player_name: str
        :param moves:
        :type moves: list
        :param status:
        :type status: str
        :return:
        :rtype: bool
        """
        player = await self.find_player(username)

        if player is None:
            return False

        player.history.append(str({"opponent": player_name, "moves": moves, "status": status}))

        await self.exec_write_query("UPDATE players SET history = $1 WHERE name = $2", (player.history, username))
        return True

    async def all_players(self) -> list[data.PlayerRecord]:
        """Get all players."""
        records = await self.exec_fetchall("SELECT * FROM players")
        return [data.PlayerRecord(*record) for record in records]
