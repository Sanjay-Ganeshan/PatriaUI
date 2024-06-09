from random import SystemRandom
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
            "(+)"
            if self.status == RollStatus.ADVANTAGE
            else "(-)"  # down arrow unicode
            if self.status == RollStatus.DISADVANTAGE
            else ""
        )

        return status_msg + msg + mod_msg

    def replace(
        self,
        faces: T.Optional[Dice] = None,
        n_dice: T.Optional[int] = None,
        modifier: T.Optional[int] = None,
        status: T.Optional[RollStatus] = None,
    ) -> "Roll":
        new_faces = faces if faces is not None else self.faces
        new_n_dice = n_dice if n_dice is not None else self.n_dice
        new_modifier = modifier if modifier is not None else self.modifier
        new_status = status if status is not None else self.status

        return Roll(
            faces=new_faces,
            n_dice=new_n_dice,
            modifier=new_modifier,
            status=new_status,
        )


@dataclass(frozen=True)
class CompletedRoll:
    roll: Roll = field(default_factory=Roll)
    raw: T.List[int] = field(default_factory=list)
    rand = SystemRandom()

    @classmethod
    def realize(cls, r: Roll) -> "CompletedRoll":
        raw = []
        n = r.n_dice
        if r.status == RollStatus.ADVANTAGE or r.status == RollStatus.DISADVANTAGE:
            n += 1

        for _ in range(n):
            raw.append(cls.rand.randrange(0, r.faces.value) + 1)

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

    def __str__(self) -> str:
        return f"{self.roll} {self.raw[:10]} => {self.total()}"
