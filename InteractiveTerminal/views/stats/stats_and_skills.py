from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.state.app_settings import BOX_WIDTH
from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges
from .skill_block import SkillTagList
from .stat_block import CharacterStatModifierBlock


class CharacterStats(MDBoxLayout, BoxSized, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH, box_height=5, orientation="vertical", **kwargs
        )
        self.box_init()
        self.listener_init()

        self.stat_mods = CharacterStatModifierBlock()
        self.add_widget(self.stat_mods)

        self.skills = SkillTagList()

        self.add_widget(self.skills)
