from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges
from kivymd.uix.boxlayout import MDBoxLayout
from ...new_models.state.app_settings import BOX_WIDTH
from .stat_badge import StatBadge
from ..shared.spacer import Spacer
from ...new_models.character.stats import Stat


class CharacterStatModifierBlock(MDBoxLayout, BoxSized, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=2,
            orientation="horizontal",
            **kwargs
        )
        self.box_init()
        self.listener_init()

        self.strength = StatBadge(which_stat=Stat.STRENGTH)
        self.dexterity = StatBadge(which_stat=Stat.DEXTERITY)
        self.intelligence = StatBadge(which_stat=Stat.INTELLIGENCE)
        self.constitution = StatBadge(which_stat=Stat.CONSTITUTION)
        self.wisdom = StatBadge(which_stat=Stat.WISDOM)

        self.wisdom_space_left = Spacer(
            box_width=self.wisdom.box_width / 2,
            box_height=self.wisdom.box_height
        )
        self.wisdom_space_right = Spacer(
            box_width=self.wisdom.box_width / 2,
            box_height=self.wisdom.box_height
        )

        self.add_widget(self.strength)
        self.add_widget(self.dexterity)
        self.add_widget(self.intelligence)
        self.add_widget(self.constitution)
        self.add_widget(self.wisdom_space_left)
        self.add_widget(self.wisdom)
        self.add_widget(self.wisdom_space_right)
