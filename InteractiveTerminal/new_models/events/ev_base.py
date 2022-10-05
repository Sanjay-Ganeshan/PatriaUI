import typing as T
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import uuid4

from ..dice.rolls import CompletedRoll
from ..state.game_state import GameState
from ..state.view_state import ViewState


@dataclass(frozen=True)
class GameOrViewEvent(ABC):
    event_id: str = field(default_factory=lambda:str(uuid4()))
    
    @abstractmethod
    def do(self, v: ViewState, g: GameState) -> T.Optional["GameOrViewEvent"]:
        """
        Performs any necessary mutations to ViewState / GameState.
        Returns an event that can be undone to undo all modifications.
        That event can be this instance OR another instance.

        (Ex: To create an event, you don't need the results of a dice roll.
             But listeners / undo, you need the result)
        """
        ...
    
    @abstractmethod
    def undo(self, v: ViewState, g: GameState) -> None:
        ...

@dataclass(frozen=True)
class ViewEvent(GameOrViewEvent):
    pass    

@dataclass(frozen=True)
class GameEvent(GameOrViewEvent):
    pass

@dataclass(frozen=True)
class RollEvent(GameEvent):
    roll: T.Optional[CompletedRoll] = None

