from ..shared.box_sized_mixin import BoxSized
from ..shared.touchable_mixin import TouchableMixin
from kivy.uix.image import Image
from ..resource_list import Resources
from ...new_models.events.view_events import SwitchFocusedView
from ...new_models.state.view_state import Views
from ..shared.listens_for_state_changes import ListenForStateChanges


class CycleViews(Image, BoxSized, TouchableMixin, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.CYCLE,
            box_width=2,
            box_height=2,
            allow_stretch=True,
            color="blue",
            **kwargs,
        )
        self.box_init()
        self.touch_init()
        self.listener_init()

    def on_left_click(self, position):
        super().on_left_click(position)
        # change characters
        if self.state_manager is not None:
            if self.state_manager.view_state.focused_view is None:
                next_view = Views.CHARACTER_DETAILS
            else:
                next_view = self.state_manager.view_state.focused_view.next()
            self.state_manager.push_event(
                SwitchFocusedView(new_focus=next_view, )
            )
