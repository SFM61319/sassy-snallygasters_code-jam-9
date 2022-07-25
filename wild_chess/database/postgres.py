"""Base database model."""


import typing

import asyncpg

__all__: tuple[str, ...] = ("DatabaseModel",)


class DatabaseModel:  # model commands class for database
    """General methods for database."""

    pool: asyncpg.pool.Pool

    async def exec_write_query(self, query: str, data: typing.Optional[tuple] = None) -> None:
        """
        Execute a write query.

        :param query:
        :type query: str
        :param data:
        :type data: typing.Optional[tuple]
        """
        if data:
            await self.pool.execute(query, *data)
            return

        await self.pool.execute(query)

    async def exec_fetchone(self, query: str, data: typing.Optional[tuple] = None) -> typing.Optional[asyncpg.Record]:
        """
        Execute a fetchone query.

        :param query:
        :type query: str
        :param data:
        :type data: typing.Optional[tuple]
        :return:
        :rtype: typing.Optional[asyncpg.Record]
        """
        result: typing.Optional[asyncpg.Record] = await self.pool.fetchrow(query, *data)
        return result

    async def exec_fetchall(self, query: str) -> list[asyncpg.Record]:
        """
        Execute a fetchall query.

        :param query:
        :type query: str
        :return:
        :rtype: list[asyncpg.Record]
        """
        results: list[asyncpg.Record] = await self.pool.fetch(query)
        return results
