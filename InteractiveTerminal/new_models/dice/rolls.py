import random
import typing as T
from dataclasses import dataclass, field

from .advantage import RollStatus
from .dice import Dice


@dataclass(frozen=True)
class Roll:
    faces: Dice = Dice.D6
    n_dice: int = 1
    modifier: int = 0
    status: RollStatus = RollStatus.STANDARD

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
