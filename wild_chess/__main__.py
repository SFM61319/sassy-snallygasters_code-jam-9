"""Main file."""


import asyncio

from wild_chess.setup import setup


async def test(test_setup: setup.Setup) -> None:
    """Tests setup"""
    await test_setup.setup()
    await test_setup.database.create_player("test")
    print(await test_setup.database.find_player("test"))
    print(await test_setup.database.all_players())
    await test_setup.database.update_player_win("test")
    print(await test_setup.database.find_player("test"))
    await test_setup.database.update_player_loss("test")
    print(await test_setup.database.find_player("test"))
    await test_setup.database.update_player_tie("test")
    print(await test_setup.database.find_player("test"))
    await test_setup.database.update_player_history("test", "user", ["00", "01", "02"], "win")
    print(await test_setup.database.find_player("test"))
    await test_setup.database.remove_player("test")
    print(await test_setup.database.all_players())
    await test_setup.database.drop_table()
    print("success")


if __name__ == "__main__":
    bot = setup.Setup()  # creating a bot object
    asyncio.run(test(bot))  # calling the test function
