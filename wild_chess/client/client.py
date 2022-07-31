"""client functions"""


import requests

url = "https://sassy-server.herokuapp.com"


def host_game(username: str) -> dict:
    """
    :param username:
    :return:
    """
    return requests.post(f"{url}/host-game?username={username}").json()


def join_game(code: str, username: str) -> dict:
    """
    :param code:
    :param username:
    :return:
    """
    return requests.post(f"{url}/join-game/{code}?username={username}").json()


def get_board(code: str, username: str) -> dict:
    """
    :param code:
    :param username:
    :return:
    """
    return requests.get(f"{url}/game/{code}?username={username}").json()


def post_board(code: str, username: str, board: dict) -> dict:
    """
    :param code:
    :param username:
    :param board:
    :return:
    """
    return requests.post(f"{url}/game/{code}?username={username}&board={board}").json()
