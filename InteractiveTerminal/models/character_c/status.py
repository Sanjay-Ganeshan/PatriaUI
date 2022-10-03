import typing as T
from dataclasses import dataclass

@dataclass(frozen=True)
class Status:
    HP: int = 12
    armor_rating: int = 14
    revives: int = 1
    deflects: int = 1
    hit_dice: int = 2
    suit_power: int = 6
    shield_power: int = 6

    death_fails: int = 2
    death_successes: int = 3