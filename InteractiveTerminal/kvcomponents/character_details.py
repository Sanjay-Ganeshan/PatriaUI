from kivymd.uix.boxlayout import MDBoxLayout

from .shared.box_sized_mixin import BoxSized
from .shared.needs_character_mixin import NeedsConstants
from ..models.app_settings import BOX_WIDTH
from .stats_and_skills import CharacterStats
from .general_controls.dice_bar import DiceBar
from .weapons.weapon_bar import WeaponBar
from .spells.spell_bar import SpellBar


class DetailsSheet(MDBoxLayout, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=10,
            orientation="vertical",
            **kwargs,
        )

        self.box_init()
        self.constants_init()

        self.stats = CharacterStats()
        self.weapon_bar = WeaponBar()
        self.spell_bar = SpellBar()
        self.dice_bar = DiceBar()
        self.add_widget(self.stats)
        self.add_widget(self.weapon_bar)
        self.add_widget(self.spell_bar)
        self.add_widget(self.dice_bar)