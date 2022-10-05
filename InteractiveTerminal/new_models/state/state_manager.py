import typing as T
from dataclasses import dataclass, field

from ..events.ev_base import GameOrViewEvent
from .game_state import GameState
from .view_state import ViewState


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

    def push_event(self, ev: T.Union[GameOrViewEvent, T.List[GameOrViewEvent]]) -> None:
        """
        Push's the given event or chain of events.

        With one event, will DO the event
        With a chain, if any of them is a no-op, will do none of them.
        If ALL succeed, will DO all of them
        """
        # After do-ing the event we might have filled more info
        # in.
        if isinstance(ev, GameOrViewEvent):
            chain = [ev]
        else:
            chain = ev

        updated_evs: T.List[GameOrViewEvent] = []
        success = True
        for each_ev in chain:
            updated = each_ev.do(self.view_state, self.game_state)
            if updated is None:
                # Something failed!
                success = False
                break
            else:
                updated_evs.append(updated)
        
        if success:
            for each_updated_ev in updated_evs:
                # Let's commit all these to history, and notify our listeners
                self._history.append(each_updated_ev)
                print("PUSH", each_updated_ev)

                for (_sub_id, each_listener) in self._listeners.items():
                    # True = do
                    each_listener(each_updated_ev, True, self)
    
        else:
            # Failed! Let's just undo everything, and forget about it
            for each_updated_ev in reversed(updated_evs):
                each_updated_ev.undo(self.view_state, self.game_state)

    def pop_event(self) -> None:
        if len(self._history) > 0:
            ev = self._history.pop()
            print("POP", ev)
            ev.undo(self.view_state, self.game_state)

            for (_sub_id, each_listener) in self._listeners.items():
                # False = undo
                each_listener(ev, False, self)

            

    
    
