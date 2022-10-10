from kivymd.uix.gridlayout import MDGridLayout
from ..shared.box_sized_mixin import BoxSized

from ..shared.listens_for_state_changes import ListenForStateChanges
from ...new_models.state.app_settings import BOX_WIDTH
from .skill_tag import SkillTag
from ..shared.spacer import Spacer
from ...new_models.character.proficiencies import Proficiency


class SkillTagList(MDGridLayout, BoxSized, ListenForStateChanges):
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
        self.listener_init()

        self.tags = {}
        all_skills = Proficiency.all()
        for each_skill in all_skills:
            self.tags[each_skill] = SkillTag(which_skill=each_skill)

        # STR
        self.add_widget(self.tags[Proficiency.ATHLETICS])
        self.add_widget(self.tags[Proficiency.COMBATIVES])
        self.add_widget(Spacer(box_width=1, box_height=1))

        # DEX
        self.add_widget(self.tags[Proficiency.ACROBATICS])
        self.add_widget(self.tags[Proficiency.STEALTH])
        self.add_widget(Spacer(box_width=2, box_height=1))

        # INT
        self.add_widget(self.tags[Proficiency.INVESTIGATION])
        self.add_widget(self.tags[Proficiency.NATURE])
        self.add_widget(self.tags[Proficiency.ANIMAL_HANDLING])

        # CON
        self.add_widget(Spacer(box_width=2, box_height=1))
        self.add_widget(Spacer(box_width=2, box_height=1))
        self.add_widget(Spacer(box_width=2, box_height=1))

        # WIS
        self.add_widget(self.tags[Proficiency.INSIGHT])
        self.add_widget(self.tags[Proficiency.MEDICINE])
        self.add_widget(self.tags[Proficiency.PERCEPTION])
        # WIS overflowing
        self.add_widget(self.tags[Proficiency.SURVIVAL])
        self.add_widget(self.tags[Proficiency.SOCIAL])
        self.add_widget(self.tags[Proficiency.INITIATIVE])
