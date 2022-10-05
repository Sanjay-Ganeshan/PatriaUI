"""
View events do NOT impact game state - they just impact how we are
displaying the UI
"""

from .ev_base import GameOrViewEvent, ViewEvent
from ..state.game_state import GameState
from ..state.view_state import ViewState, Views

from dataclasses import dataclass
import typing as T


@dataclass(frozen=True)
class SwitchFocusedCharacter(ViewEvent):
    # Need for create
    new_focus: T.Optional[str] = None

    # We'll fix these
    old_focus: T.Optional[str] = None

    def do(self, v: ViewState, g: GameState) -> GameOrViewEvent:
        prev_focus = v.focused_character
        v.focused_character = self.new_focus
        return SwitchFocusedCharacter(
            event_id=self.event_id,
            old_focus=prev_focus,
            new_focus=self.new_focus,
        )

    def undo(self, v: ViewState, g: GameState):
        assert v.focused_character == self.new_focus, "Invalid event order"
        v.focused_character = self.old_focus


@dataclass(frozen=True)
class SwitchFocusedView(ViewEvent):
    # Need for create
    new_focus: Views = Views.EMPTY

    # We'll fix these
    old_focus: Views = Views.EMPTY

    def do(self, v: ViewState, g: GameState) -> GameOrViewEvent:
        prev_focus = v.focused_view
        v.focused_view = self.new_focus
        return SwitchFocusedView(
            event_id=self.event_id,
            old_focus=prev_focus,
            new_focus=self.new_focus,
        )

    def undo(self, v: ViewState, g: GameState):
        assert v.focused_view == self.new_focus, "Invalid event order"
        v.focused_view = self.old_focus
