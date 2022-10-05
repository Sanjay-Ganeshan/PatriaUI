from kivymd.uix.boxlayout import MDBoxLayout

from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges
from ...new_models.state.app_settings import BOX_WIDTH
from ..stats.stats_and_skills import CharacterStats


class DetailsSheet(MDBoxLayout, BoxSized, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=10,
            orientation="vertical",
            **kwargs,
        )

        self.box_init()
        self.listener_init()

        self.stats = CharacterStats()
        self.add_widget(self.stats)
