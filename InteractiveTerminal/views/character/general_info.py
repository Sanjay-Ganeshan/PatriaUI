from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.character.stats import Stat
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.state.app_settings import BOX_WIDTH
from ...new_models.state.state_manager import StateManager
from ..resource_list import Resources
from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..stats.stat_badge import StatBadge
from .armor import CHArmor
from .icon import CHIcon
from .life_and_death import CHLife
from .name_and_role import CHNamecard
from .power import CHPower
from .restoration import CHRestoration


class CHGeneralInfo(MDBoxLayout, BoxSized, ListenForStateChanges):
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
        self.listener_init()

        self.icon = CHIcon()
        self.namecard = CHNamecard()
        self.armor = CHArmor()
        self.power = CHPower()
        self.life = CHLife()
        self.restoration = CHRestoration()
        self.proficiency = StatBadge(
            which_stat=Stat.PROFICIENCY_BONUS,
            source=Resources.PROFICIENCY_STAT_ICON,
            box_height=3,
            pr_full_color="white",
        )

        self.add_widget(self.icon)
        self.add_widget(self.namecard)
        self.add_widget(self.armor)
        self.add_widget(self.power)
        self.add_widget(self.life)
        self.add_widget(self.restoration)
        self.add_widget(self.proficiency)

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        pass
