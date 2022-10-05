from enum import Enum, unique

@unique
class Buffs(Enum):
    # Grants access to the "designate" ability
    LEADERSHIP = "leadership"

@unique
class Debuffs(Enum):
    # Trimmed skinsuit - reduces armor rating by 2
    # and maximum power by 3
    SLIM_SKINSUIT = "slim_skinsuit"

    # Reduces all incoming healing by 1
    HARD_TO_TREAT = "hard_to_treat"
