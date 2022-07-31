"""multiplayer functions"""

from fastapi import APIRouter
from random import shuffle


route = APIRouter()
active_game = {}


@route.post('/host-game')
async def host_game(username: str) -> dict:
    """
    :param username:
    :return:
    """
    code: list[str] = [str(i) for i in range(6)]
    shuffle(code)
    shuffled: str = "".join(code)
    active_game[username] = {'code': shuffled, 'board': None, 'players': [username]}
    return {'code': code}


@route.post('/join-game/{code}')
async def join_game(code: str, username: str) -> dict:
    """
    :param code:
    :param username:
    :return:
    """
    for k, v in active_game.items():
        if v['code'] == code:
            if len(v['players']) == 1 and username not in v['players']:
                v['players'].append(username)
                return {'message': 'ok'}

    return {'message': 'error'}


@route.post('/game/{code}')
async def post_game(code: str, username: str, board: list[list[str]]) -> dict:
    """
    :param code:
    :param username:
    :param board:
    :return:
    """
    for i in active_game:
        if active_game[i]['code'] == code and username in active_game[i]['players']:
            active_game[i]['board'] = board
            return {'message': 'ok'}

    return {'message': 'error'}


@route.get('/game/{code}')
async def get_board(code: str, username: str) -> dict:
    """
    :param code:
    :param username:
    :return:
    """
    for i in active_game:
        if active_game[i]['code'] == code and username in active_game[i]['players']:
            return {'board': active_game[i]['board']}

    return {'board': 'error'}
