"""Data classes."""


from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class PlayerRecord:
    """
    PlayerRecord is a dataclass that represents a player's record in the database.

    It is used to store the player's name, wins, losses, ties, and history.
    """

    player_name: str
    password: str
    wins: int
    losses: int
    ties: int
    history: list[str | None]


@dataclasses.dataclass
class PlayerAttributes:
    """PlayerAttributes is a dataclass that represents a player's attributes."""

    name: str
    color: str
