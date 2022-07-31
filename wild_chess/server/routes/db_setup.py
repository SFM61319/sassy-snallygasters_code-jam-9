"""db setup file"""
import asyncio

from wild_chess.setup.setup import Setup


async def main():
    return await Setup().setup()

db = asyncio.run(main())
