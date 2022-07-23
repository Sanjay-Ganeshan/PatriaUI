from kivymd.uix.boxlayout import MDBoxLayout

from .cycle_views import CycleViews
from .game_log_window import GameLogView
from ..shared.box_sized_mixin import BoxSized
from ...utils import use_passed_or_default
from ...models.app_settings import BOX_WIDTH

class GameLogAndControls(MDBoxLayout, BoxSized):
    def __init__(self, **kwargs):
        super().__init__(
            **use_passed_or_default(
                kwargs,
                box_width = BOX_WIDTH,
                box_height=2,
                orientation="horizontal",
            )
        )
        self.box_init()

        self.controls = CycleViews()
        self.game_log_view = GameLogView()

        self.add_widget(self.controls)
        self.add_widget(self.game_log_view)