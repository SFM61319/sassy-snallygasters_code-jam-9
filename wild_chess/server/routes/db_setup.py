"""db setup file"""
import asyncio

from ...setup.setup import Setup

async def main():
    return await Setup().setup()

db = asyncio.run(main())
