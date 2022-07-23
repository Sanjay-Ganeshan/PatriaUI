from enum import IntEnum, unique
import random
import typing as T

from .game import THE_GAME
from .roll_status import RollStatus

@unique
class Dice(IntEnum):
    D2 = 2
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20



def roll(
    faces: Dice,
    n_dice: int = 1,
    modifier: int = 0,
    description: str = "",
    roll_type: T.Optional[RollStatus] = None,
    post_roll_desc: T.Optional[T.Callable[[T.Tuple[int, T.List[int]]], str]] = None,
) -> T.Tuple[int, T.List[int]]:

    if roll_type is None:
        roll_type = THE_GAME.get_current_character().NEXT_ROLL_STATUS
        THE_GAME.change_roll_status(RollStatus.STANDARD)

    rolled_vals = []
    for i in range(n_dice + (1 if roll_type != RollStatus.STANDARD else 0)):
        rolled_vals.append(random.randrange(1, faces.value + 1))

    orig_rolls = rolled_vals[:]

    if roll_type != RollStatus.STANDARD:
        which_to_drop = (
            min(rolled_vals) if roll_type == RollStatus.ADVANTAGE else max(rolled_vals)
        )
        rolled_vals.remove(which_to_drop)
    
    roll_total = sum(rolled_vals)
    roll_total_with_modifier = roll_total + modifier
    
    msg = (
        f"{description}. {roll_total_with_modifier}!\n"
        f"Rolled {n_dice}d{faces.value}{modifier:+d} -- "
        f"Raw rolls: {orig_rolls}"
    )

    if roll_type != RollStatus.STANDARD:
        msg = f"{msg} at {roll_type.value}, dropping {which_to_drop}"
    
    msg = f"{msg} -- Total:{roll_total}{modifier:+d} ==> {roll_total_with_modifier}"

    if post_roll_desc is not None:
        suffix = "\n" + post_roll_desc(roll_total, rolled_vals)
    else:
        suffix = ""
    THE_GAME.game_log.log(msg + suffix)

    return roll_total_with_modifier, rolled_vals

