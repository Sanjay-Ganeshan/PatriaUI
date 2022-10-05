from dataclasses import dataclass, field
import typing as T

from .game_state import GameState
from .view_state import ViewState

from ..events.ev_base import GameOrViewEvent

@dataclass
class StateManager:

    view_state: ViewState = field(default_factory=ViewState)
    game_state: GameState = field(default_factory=GameState)

    _next_subscription_id: int = field(default=0, metadata={"IGNORESAVE": True})
    _listeners: T.Dict[int, T.Callable[[GameOrViewEvent, bool, "StateManager"], None]] = field(default_factory=dict, metadata={"IGNORESAVE": True})
    _history: T.List[GameOrViewEvent] = field(default_factory=list, metadata={"IGNORESAVE": True})

    def subscribe(self, callback: T.Callable[[GameOrViewEvent, bool, "StateManager"], None]) -> int:
        """
        Add a listener that will be called every time we process
        *any* event. You need to filter to which events you care
        about.

        Returns an ID. If you call unsubscribe() with this ID, we'll
        stop listening

        Your callback will be called with the args:
        (event instance, is_do, state_manager after process)

        is_do is True when we're going forward through the event,
        and False when we're undoing the event.
        """
        self._listeners[self._next_subscription_id] = callback
        ret = self._next_subscription_id
        self._next_subscription_id += 1

        return ret


    def unsubscribe(self, sub_id: int) -> bool:
        """
        If the given subscription ID is valid, unsubscribes it.
        Returns True if we cancelled a subscription
        """
        return self._listeners.pop(sub_id, None) is not None

    def push_event(self, ev: GameOrViewEvent) -> None:
        # After do-ing the event we might have filled more info
        # in.
        ev = ev.do(self.view_state, self.game_state)
        self._history.append(ev)

        for (_sub_id, each_listener) in self._listeners.items():
            # True = do
            each_listener(ev, True, self)

    def pop_event(self) -> None:
        if len(self._history) > 0:
            ev = self._history.pop()
            ev.undo(self.v, self.g)

            for (_sub_id, each_listener) in self._listeners.items():
                # False = undo
                each_listener(ev, False, self)


    
    
