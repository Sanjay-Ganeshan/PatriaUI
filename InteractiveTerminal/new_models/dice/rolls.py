import random
import typing as T
from dataclasses import dataclass, field

from .advantage import RollStatus
from .dice import Dice, Critical


@dataclass(frozen=True)
class Roll:
    faces: Dice = Dice.D6
    n_dice: int = 1
    modifier: int = 0
    status: RollStatus = RollStatus.STANDARD

    def __str__(self) -> str:
        msg = f"{self.n_dice}d{self.faces.value}"
        mod_msg = "" if self.modifier == 0 else f"{self.modifier:+d}"
        status_msg = (
            chr(24)  # up arrow ASCII
            if self.status == RollStatus.ADVANTAGE
            else chr(25)  # down arrow ASCII
            if self.status == RollStatus.DISADVANTAGE
            else " "
        )

        return status_msg + mod_msg + msg


@dataclass(frozen=True)
class CompletedRoll:
    roll: Roll = field(default_factory=Roll)
    raw: T.List[int] = field(default_factory=list)

    @classmethod
    def realize(cls, r: Roll) -> "CompletedRoll":
        raw = []
        n = r.n_dice
        if r.status == RollStatus.ADVANTAGE or r.status == RollStatus.DISADVANTAGE:
            n += 1

        for _ in range(r.n_dice):
            raw.append(random.randrange(0, r.faces.value) + 1)

        return cls(roll=r, raw=raw)

    def is_critical(self) -> Critical:
        if self.roll.n_dice == 1 and self.roll.faces == Dice.D20:
            if self.total() - self.roll.modifier == 20:
                return Critical.SUCCESS
            elif self.total() - self.roll.modifier == 1:
                return Critical.FAILURE
            else:
                return Critical.NO
        else:
            return Critical.NO

    def total(self) -> int:
        tot = sum(self.raw)
        if self.roll.status == RollStatus.ADVANTAGE:
            # Drop the lowest
            tot -= min(self.raw)
        elif self.roll.status == RollStatus.DISADVANTAGE:
            # Drop the highest
            tot -= max(self.raw)

        tot += self.roll.modifier
        return tot
