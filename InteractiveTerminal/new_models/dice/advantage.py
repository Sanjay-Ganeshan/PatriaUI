from enum import Enum, unique
import typing as T


@unique
class RollStatus(Enum):
    STANDARD = "standard"
    DISADVANTAGE = "disadvantage"
    ADVANTAGE = "advantage"

    def apply(self, other: "RollStatus") -> T.Tuple["RollStatus", "RollStatus"]:
        """
        If self is the active character's next roll status, and "other"
        is the status of the active roll, returns

        Return (new next roll status, new status for active roll)
        """
        assert isinstance(other, RollStatus), f"{other} is not a RollStatus"
        if self == RollStatus.STANDARD:
            return (self, other)
        elif self == other:
            # Advantage / advantage .. can't gain double
            return (self, other)
        elif other == RollStatus.STANDARD:
            # Consume me to boost / debuff the roll
            return (RollStatus.STANDARD, self)
        else:
            # Cancel out
            return (RollStatus.STANDARD, RollStatus.STANDARD)
