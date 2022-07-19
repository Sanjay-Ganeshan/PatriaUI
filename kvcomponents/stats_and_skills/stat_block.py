from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants
from kivymd.uix.boxlayout import MDBoxLayout
from ...models.app_settings import BOX_WIDTH
from .stat_tag import StatDesignation
from ..shared.spacer import Spacer

class CharacterStatModifierBlock(MDBoxLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH, box_height=2, orientation="horizontal", **kwargs
        )
        self.box_init()
        self.constants_init()

        self.strength = StatDesignation(stat_name="STRENGTH")
        self.dexterity = StatDesignation(stat_name="DEXTERITY")
        self.intelligence = StatDesignation(stat_name="INTELLIGENCE")
        self.constitution = StatDesignation(stat_name="CONSTITUTION")
        self.wisdom = StatDesignation(stat_name="WISDOM")
        self.wisdom_space_left = Spacer(
            box_width=self.wisdom.box_width / 2, box_height=self.wisdom.box_height
        )
        self.wisdom_space_right = Spacer(
            box_width=self.wisdom.box_width / 2, box_height=self.wisdom.box_height
        )

        self.add_widget(self.strength)
        self.add_widget(self.dexterity)
        self.add_widget(self.intelligence)
        self.add_widget(self.constitution)
        self.add_widget(self.wisdom_space_left)
        self.add_widget(self.wisdom)
        self.add_widget(self.wisdom_space_right)
