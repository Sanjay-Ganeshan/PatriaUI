from enum import Enum
import typing as T


class Spell(Enum):
    INCINERATE = "INCINERATE"
    ELECTROCUTE = "ELECTROCUTE"
    FREEZE = "FREEZE"
    WARP = "WARP"
    DEFLECT = "DEFLECT"
    REPULSE = "REPULSE"
    FEEDBACK = "FEEDBACK"
    TELEKINESIS = "TELEKINESIS"

    @classmethod
    def all(cls) -> T.List["Spell"]:
        return list(cls.__members__.values())
