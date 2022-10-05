from enum import Enum, unique


@unique
class RollStatus(Enum):
    STANDARD = "standard"
    DISADVANTAGE = "disadvantage"
    ADVANTAGE = "advantage"
