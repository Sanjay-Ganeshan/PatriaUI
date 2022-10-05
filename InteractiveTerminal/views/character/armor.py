
from kivy.properties import NumericProperty

from ...new_models.character.character import Character
from ...new_models.character.status import Status
from ...new_models.events.abilities import (cast_reactive_armor,
                                            expire_reactive_armor)
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.help import help_generator
from ...new_models.state.state_manager import StateManager
from ..resource_list import Resources
from ..shared.centered_label import CenteredLabel
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..shared.progressive_icon import ProgressiveIconImpl
from ..shared.touchable_mixin import TouchableMixin


# Not a kivy image because we want the text on top
class CHArmor(CenteredLabel, ProgressiveIconImpl, ListenForStateChanges, TouchableMixin):
    base_armor: int = NumericProperty(0)
    current_armor: int = NumericProperty(0)
    
    def __init__(self, **kwargs):
        """
        Displays your armor rating prominently
        """
        super().__init__(
            # Sizing
            box_height=3,
            box_width=1.5,
            # Centered Text
            text="",
            # Icon in back
            source=Resources.ARMOR_ICON,
            maximum_value=1,
            current_value=1,
            pr_empty_color="black",
            pr_full_color="black",
            stacked=False,
            **kwargs,
        )
        self.listener_init()
        self.progressive_init()
        self.touch_init()

        self.bind(base_armor=self.armor_rating_updated, current_armor=self.armor_rating_updated)

    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.base_armor = 0
            self.current_armor = 0
        else:
            char: Character = state_manager.game_state.characters[state_manager.view_state.focused_character]
            current: Status = char.current_life
            maxi: Status = char.max_life

            self.current_armor = current.armor_rating
            self.base_armor = maxi.armor_rating



    def armor_rating_updated(self, *args):
        # change color to indicate buffed / debuffed
        if self.current_armor == self.base_armor:
            self.pr_full_color = "black"
        elif self.current_armor < self.base_armor:
            self.pr_full_color = "#de968e"
        else:
            self.pr_full_color = "#8ede9f"
        
        self.text = f"Armor\n{self.current_armor}"
        self.tooltip_text = help_generator.armor_rating(
            self.current_armor,
            self.base_armor,
        )

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.state_manager is None:
            return
        
        if self.state_manager.view_state.focused_character is None:
            return

        # Left click -> Cast Reactive Armor
        self.state_manager.push_event(cast_reactive_armor(self.state_manager.view_state.focused_character))

    def on_right_click(self, *args):
        super().on_right_click(*args)
        
        if self.state_manager is None:
            return
        
        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(expire_reactive_armor(self.state_manager.view_state.focused_character))
