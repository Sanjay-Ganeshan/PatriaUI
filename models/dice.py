from enum import IntEnum, unique
import random
import typing as T

from .roll_status import RollStatus
from dataclasses import dataclass, replace

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
    from .game import THE_GAME

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
    
    crit_string = ""
    if len(rolled_vals) == 1 and faces == Dice.D20:
        if 20 in rolled_vals:
            crit_string = " Critical!!"
        elif 1 in rolled_vals:
            crit_string = " Critical Failure!!"
    
    roll_total = sum(rolled_vals)
    roll_total_with_modifier = roll_total + modifier
    
    msg = (
        f"{description}. {roll_total_with_modifier}!{crit_string}\n"
        f"Rolled {n_dice}d{faces.value}{modifier:+d} -- "
        f"Raw rolls: {orig_rolls[:10]}"
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

@dataclass(frozen=True)
class RollParams:
    faces: Dice
    n_dice: int = 1
    modifier: int = 0
    roll_type: T.Optional[RollStatus] = None
    description: str = ""
    post_roll_desc: T.Optional[T.Callable[[T.Tuple[int, T.List[int]]], str]] = None

    def roll(self) -> T.Tuple[int, T.List[int]]:
        return roll(
            faces=self.faces,
            n_dice=self.n_dice,
            modifier=self.modifier,
            roll_type=self.roll_type,
            description=self.description,
            post_roll_desc=self.post_roll_desc,
        )
    
    def replace(
        self, 
        faces: T.Optional[Dice] = None,
        n_dice: T.Optional[int]=None,
        modifier: T.Optional[int] = None,
        roll_type: T.Optional[RollStatus] = None,
        description: T.Optional[str] = None,
        post_roll_desc: T.Optional[str] = None,
    ) -> "RollParams":
        changes = {}
        if faces is not None:
            changes["faces"] = faces
        if n_dice is not None:
            changes["n_dice"] = n_dice
        if modifier is not None:
            changes["modifier"] = modifier
        if roll_type is not None:
            changes["roll_type"] = roll_type
        if description is not None:
            changes["description"] = description
        if post_roll_desc is not None:
            changes["post_roll_desc"] = post_roll_desc

        return replace(self, **changes)
    
    def __str__(self) -> str:
        from .game import THE_GAME
        if self.roll_type is None:
            roll_type = THE_GAME.get_current_character().NEXT_ROLL_STATUS
        else:
            roll_type = roll_type
        
        if roll_type == RollStatus.STANDARD:
            prefix = ""
        elif roll_type == RollStatus.ADVANTAGE:
            prefix = "+|"
        elif roll_type == RollStatus.DISADVANTAGE:
            prefix = "-|"
        suffix = "" if self.modifier == 0 else f"{self.modifier:+d}"
        return f"{prefix}{self.n_dice}d{self.faces.value}{suffix}"