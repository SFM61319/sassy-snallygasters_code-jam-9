import typing as t

import asyncpg

__all__: t.Tuple[str, ...] = ("DatabaseModel",)


class DatabaseModel:  # model commands class for database
    """
    General methods for database.
    """

    pool: asyncpg.pool.Pool

    async def exec_write_query(self, query: str, data: t.Tuple[t.Any, ...] | None = None) -> None:
        """
        Execute a write query.
        :param query:
        :param data:
        :return:
        """
        if data:
            await self.pool.execute(query, *data)
            return
        await self.pool.execute(query)

    async def exec_fetchone(self, query: str, data: t.Tuple[t.Any, ...] | None = None) -> t.Optional[asyncpg.Record]:
        """
        Execute a fetchone query.
        :param query:
        :param data:
        :return:
        """
        return await self.pool.fetchrow(query, *data)

    async def exec_fetchall(self, query: str) -> t.List[asyncpg.Record]:
        """
        Execute a fetchall query.
        :param query:
        :return:
        """
        return await self.pool.fetch(query)
