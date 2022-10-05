from enum import Enum, IntEnum, unique


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
class Critical(Enum):
    NO = "NO"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

    def msg(self) -> str:
        """
        Easy to add-on msg
        """
        if self == Critical.SUCCESS:
            return " Critical!!"
        if self == Critical.FAILURE:
            return " Critical Failure!!"
        else:
            return ""