"""
Game events actually impact game state
"""

from .ev_base import GameEvent, RollEvent
from dataclasses import dataclass

@dataclass(frozen=True)
class DeathSave(RollEvent):
    pass

@dataclass(frozen=True)
class StatTest(RollEvent):
    pass

@dataclass(frozen=True)
class SkillTest(RollEvent):
    pass

@dataclass(frozen=True)
class ChangeHP(GameEvent):
    pass

@dataclass(frozen=True)
class ChangePower(GameEvent):
    pass

@dataclass(frozen=True)
class ChangeShield(GameEvent):
    pass

@dataclass(frozen=True)
class UseHitDice(GameEvent):
    pass

@dataclass(frozen=True)
class SkillTest(GameEvent):
    pass

@dataclass(frozen=True)
class SkillTest(GameEvent):
    pass





