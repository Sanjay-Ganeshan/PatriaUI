from kivymd.uix.gridlayout import MDGridLayout
from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants
from ...models.app_settings import BOX_WIDTH
from .skill_tag import SkillTag
from collections import OrderedDict
from ...models.character import Constants
from ..shared.spacer import Spacer

class SkillTagList(MDGridLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        N_ROWS = 3
        super().__init__(
            orientation="tb-lr",
            box_width=BOX_WIDTH,
            box_height=N_ROWS,
            cols=BOX_WIDTH // 2,
            rows=N_ROWS,
            **kwargs,
        )
        self.box_init()
        self.constants_init()

        self.tags = OrderedDict()
        all_skills = Constants.list_skills()
        for skill_name in all_skills:
            self.tags[skill_name] = SkillTag(skill_name=skill_name)

        # STR
        self.add_widget(self.tags["STR_ATHLETICS"])
        self.add_widget(self.tags["STR_COMBATIVES"])
        self.add_widget(Spacer(box_width=1, box_height=1))
        # DEX
        self.add_widget(self.tags["DEX_ACROBATICS"])
        self.add_widget(self.tags["DEX_STEALTH"])
        self.add_widget(Spacer(box_width=2, box_height=1))
        # INT
        self.add_widget(self.tags["INT_INVESTIGATION"])
        self.add_widget(self.tags["INT_NATURE"])
        self.add_widget(self.tags["INT_ANIMAL_HANDLING"])
        # CON
        self.add_widget(Spacer(box_width=2, box_height=1))
        self.add_widget(Spacer(box_width=2, box_height=1))
        self.add_widget(Spacer(box_width=2, box_height=1))
        # WIS
        self.add_widget(self.tags["WIS_INSIGHT"])
        self.add_widget(self.tags["WIS_MEDICINE"])
        self.add_widget(self.tags["WIS_PERCEPTION"])
        # WIS overflowing into PROF
        self.add_widget(self.tags["WIS_SURVIVAL"])
        self.add_widget(self.tags["WIS_SOCIAL"])
        self.add_widget(Spacer(box_width=2, box_height=1))
