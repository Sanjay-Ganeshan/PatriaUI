from kivy.properties import NumericProperty, ObjectProperty

from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.state.state_manager import StateManager


class ListenForStateChanges:
    state_manager: StateManager = ObjectProperty(None, allownone=True)
    _subscription_id: int = NumericProperty(-1)

    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        pass

    def _state_manager_updated(self, *args):
        to_update = []
        if hasattr(self, "children"):
            for each_child in self.children:
                if isinstance(each_child, ListenForStateChanges):
                    to_update.append(each_child)
        for each_attr in dir(self):
            possible_child = getattr(self, each_attr)
            if (
                isinstance(possible_child, ListenForStateChanges)
                and possible_child not in to_update
            ):
                to_update.append(possible_child)

        for each_update in to_update:
            each_update.state_manager = self.state_manager

        self._subscription_id = self.state_manager.subscribe(self.listener)

    def listener_init(self):
        self.bind(state_manager=self._state_manager_updated)
