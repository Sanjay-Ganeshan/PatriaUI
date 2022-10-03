from kivymd.uix.boxlayout import MDBoxLayout
from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants

from ...models.app_settings import BOX_HEIGHT, BOX_WIDTH
from .character_icon import CHIcon
from .character_namecard import CHNamecard
from .character_armor import CHArmor
from ..stats_and_skills.stat_tag import StatDesignation
from .character_power import CHPower
from .character_restoration_abilities import CHRestoration
from .character_life import CHLife
from ..resource_list import Resources


class CharacterGeneralInfo(MDBoxLayout, BoxSized, NeedsConstants):
    """
    Info needed at a glance
    """

    def __init__(self, **kwargs):
        super().__init__(
            orientation="horizontal",
            box_width=BOX_WIDTH,
            box_height=3,
            **kwargs,
        )
        self.box_init()
        self.constants_init()
        self.icon = CHIcon()
        self.namecard = CHNamecard()
        self.armor_indicator = CHArmor()
        self.proficiency = StatDesignation(
            stat_name="PROFICIENCY_BONUS",
            source=Resources.PROFICIENCY_STAT_ICON,
            box_height=3,
            pr_full_color="white",
        )
        self.power = CHPower()
        self.life = CHLife()
        self.restoration = CHRestoration()

        self.add_widget(self.icon)
        self.add_widget(self.namecard)
        self.add_widget(self.armor_indicator)
        self.add_widget(self.power)
        self.add_widget(self.life)
        self.add_widget(self.restoration)
        self.add_widget(self.proficiency)

