from enum import IntEnum, unique, Enum
import random
import typing as T

from .game import THE_GAME

@unique
class Dice(IntEnum):
    D2 = 2
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20


@unique
class RollStatus(Enum):
    STANDARD = "standard"
    DISADVANTAGE = "disadvantage"
    ADVANTAGE = "advantage"


def roll(
    faces: Dice,
    n_dice: int = 1,
    modifier: int = 0,
    description: str = "",
    roll_type=RollStatus.STANDARD,
) -> T.Tuple[int, T.List[int]]:
    rolled_vals = []
    for i in range(n_dice + (1 if roll_type != RollStatus.STANDARD else 0)):
        rolled_vals.append(random.randrange(1, faces.value + 1))

    msg = (
        f"{description}. Rolled {n_dice}d{faces.value}+{modifier}\n"
        f"Raw rolls: {rolled_vals}"
    )

    if roll_type != RollStatus.STANDARD:
        which_to_drop = (
            min(rolled_vals) if roll_type == RollStatus.ADVANTAGE else max(rolled_vals)
        )
        rolled_vals.remove(which_to_drop)
        msg = f"{msg} at {roll_type.value}, dropping {which_to_drop}"

    roll_total = sum(rolled_vals)
    msg = f"{msg}\nTotal:{roll_total}{modifier:+d} ==> {roll_total+modifier}"

    THE_GAME.game_log.log(msg)
    return roll_total, rolled_vals

