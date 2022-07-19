from kivymd.uix.boxlayout import MDBoxLayout
from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants
from ...models.app_settings import BOX_WIDTH
from .stat_block import CharacterStatModifierBlock
from .skill_block import SkillTagList

class CharacterStats(MDBoxLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH, box_height=5, orientation="vertical", **kwargs
        )
        self.box_init()
        self.constants_init()

        self.stat_mods = CharacterStatModifierBlock()
        self.add_widget(self.stat_mods)

        self.skills = SkillTagList()

        self.add_widget(self.skills)
