from ..shared.progressive_icon import ProgressiveIcon, ProgressiveText
from ..shared.box_sized_mixin import BoxSized
from ..shared.touchable_mixin import TouchableMixin
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..shared.spacer import Spacer
from kivymd.uix.boxlayout import MDBoxLayout

from ..resource_list import Resources
from ...new_models.state.app_settings import BOX_WIDTH
from ...new_models.dice.advantage import RollStatus
from ...new_models.dice.dice import Dice
from ...new_models.state.state_manager import StateManager
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.character.character import Character
from ...new_models.events.game_events import ToggleAdvantage, ToggleDisadvantage, RandomRoll
from ...new_models.help import help_generator

from kivy.properties import ObjectProperty


class AnyDiceRoller(ProgressiveText, TouchableMixin, ListenForStateChanges):
    faces: Dice = ObjectProperty(Dice.D6)
    
    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.DICE_ICONS[Dice.D6],
            current_value=6,
            maximum_value=6,
            pr_full_color="coral",
            box_width=1,
            box_height=1,
            bold=True,
            text_color="white",
            theme_text_color="Custom",
            **kwargs,
        )
        self.touch_init()
        self.listener_init()
        self.bind(faces=self.adjust_sides)
        self.adjust_sides()

    def get_text(self) -> str:
        return str(self.maximum_value)

    def adjust_sides(self, *args):
        self.source = Resources.DICE_ICONS[self.faces]
        self.maximum_value = self.faces.value
        self.current_value = self.maximum_value

    def on_left_click(self, *args):
        super().on_left_click(*args)
        if self.state_manager is None:
            return
        
        if self.state_manager.view_state.focused_character is None:
            return
        
        self.state_manager.push_event(
            RandomRoll(
                character_id=self.state_manager.view_state.focused_character,
                faces=self.faces,
            )
        )


class AdvantageRoll(ProgressiveIcon, TouchableMixin, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.ADVANTAGE,
            current_value=0,
            maximum_value=1,
            pr_full_color="green",
            pr_empty_color="white",
            box_width=1,
            box_height=1,
            **kwargs,
        )
        self.touch_init()
        self.listener_init()

    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        if state_manager.view_state.focused_character is None:
            self.current_value = 0
            self.tooltip_text = help_generator.roll_status(RollStatus.ADVANTAGE, RollStatus.STANDARD)

        else:
            char: Character = state_manager.game_state.characters[state_manager.view_state.focused_character]
            if char.next_roll_status == RollStatus.ADVANTAGE:
                self.current_value = 1
            else:
                self.current_value = 0
            
            self.tooltip_text = help_generator.roll_status(RollStatus.ADVANTAGE, char.next_roll_status)


    def on_left_click(self, *args):
        if self.state_manager is None:
            return
        
        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(ToggleAdvantage(character_id=self.state_manager.view_state.focused_character))
        
        
class DisadvantageRoll(ProgressiveIcon, TouchableMixin, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.DISADVANTAGE,
            current_value=0,
            maximum_value=1,
            pr_full_color="red",
            pr_empty_color="white",
            box_width=1,
            box_height=1,
            **kwargs,
        )
        self.touch_init()
        self.listener_init()

    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        if state_manager.view_state.focused_character is None:
            self.current_value = 0
            self.tooltip_text = help_generator.roll_status(RollStatus.DISADVANTAGE, RollStatus.STANDARD)

        else:
            char: Character = state_manager.game_state.characters[state_manager.view_state.focused_character]
            if char.next_roll_status == RollStatus.DISADVANTAGE:
                self.current_value = 1
            else:
                self.current_value = 0
            
            self.tooltip_text = help_generator.roll_status(RollStatus.DISADVANTAGE, char.next_roll_status)


    def on_left_click(self, *args):
        if self.state_manager is None:
            return
        
        if self.state_manager.view_state.focused_character is None:
            return

        self.state_manager.push_event(ToggleDisadvantage(character_id=self.state_manager.view_state.focused_character))



class DiceBar(MDBoxLayout, BoxSized, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=1,
            orientation="horizontal",
            **kwargs,
        )
        self.box_init()
        self.listener_init()

        self.d2 = AnyDiceRoller(faces=Dice.D2)
        self.d4 = AnyDiceRoller(faces=Dice.D4)
        self.d6 = AnyDiceRoller(faces=Dice.D6)
        self.d8 = AnyDiceRoller(faces=Dice.D8)
        self.d10 = AnyDiceRoller(faces=Dice.D10)
        self.d12 = AnyDiceRoller(faces=Dice.D12)
        self.d20 = AnyDiceRoller(faces=Dice.D20)
        self.adv = AdvantageRoll()
        self.disadv = DisadvantageRoll()
        self.lspace = Spacer(box_width=1.5, box_height=1)
        self.rspace = Spacer(box_width=1.5, box_height=1)

        self.add_widget(self.lspace)
        self.add_widget(self.disadv)
        self.add_widget(self.adv)
        self.add_widget(self.d2)
        self.add_widget(self.d4)
        self.add_widget(self.d6)
        self.add_widget(self.d8)
        self.add_widget(self.d10)
        self.add_widget(self.d12)
        self.add_widget(self.d20)
        self.add_widget(self.rspace)
