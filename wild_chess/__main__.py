"""Main file."""


import asyncio

from wild_chess.setup import Setup


async def test(setup: Setup) -> None:
    """Tests setup"""
    await setup.setup()
    await setup.database.create_player("test")
    print(await setup.database.find_player("test"))
    print(await setup.database.all_players())
    await setup.database.update_player_win("test")
    print(await setup.database.find_player("test"))
    await setup.database.update_player_loss("test")
    print(await setup.database.find_player("test"))
    await setup.database.update_player_tie("test")
    print(await setup.database.find_player("test"))
    await setup.database.update_player_history("test", "user", ["00", "01", "02"], "win")
    print(await setup.database.find_player("test"))
    await setup.database.remove_player("test")
    print(await setup.database.all_players())
    await setup.database.drop_table()
    print("success")


if __name__ == "__main__":
    bot = Setup()  # creating a bot object
    asyncio.run(test(bot))  # calling the test function
