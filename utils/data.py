from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class PlayerRecord:  #model for player data
    """
    PlayerRecord is a dataclass that represents a player's record in the database.
    It is used to store the player's name, wins, losses, ties, and history.
    """
    player_name: str
    wins: int
    losses: int
    ties: int
    history: List[str | None]
