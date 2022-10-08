from enum import Enum, unique
import typing as T

@unique
class RollStatus(Enum):
    STANDARD = "standard"
    DISADVANTAGE = "disadvantage"
    ADVANTAGE = "advantage"