import typing as T

from kivy.properties import BooleanProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout

from ...new_models.character.character import Character
from ...new_models.character.status import Status
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.events.game_events import (
    ChangeDeathFail, ChangeDeathSuccess, ChangeHP, DeathSave
)
from ...new_models.help import help_generator
from ...new_models.state.state_manager import StateManager
from ..resource_list import Resources
from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges
from ..shared.progressive_icon import ProgressiveIcon, ProgressiveText
from ..shared.touchable_mixin import TouchableMixin


class CHDeathFails(ProgressiveIcon, ListenForStateChanges, TouchableMixin):
    current_death_fails: int = NumericProperty(0)
    max_death_fails: int = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=2 / 3,
            box_height=self.box_height,
            source=Resources.DEATH_FAIL,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="darkred",
            orientation="horizontal",
        )
        self.touch_init()
        self.listener_init()

        self.bind(
            current_death_fails=self.update_fails,
            max_death_fails=self.update_fails
        )
        self.update_fails()

    def update_fails(self, *args):
        self.current_value = self.current_death_fails
        self.maximum_value = self.max_death_fails

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.current_death_fails = 0
            self.max_death_fails = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            current: Status = char.current_life
            maxi: Status = char.max_life

            # Invert this. The # of death fails we have until
            # we die is what we track. We want to display
            # the number we've failed so far

            self.current_death_fails = maxi.death_fails - current.death_fails
            self.max_death_fails = maxi.death_fails

    def on_left_click(self, *args):
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return

        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(
            ChangeDeathFail(character_id=char_id, amount=-1)
        )

    def on_right_click(self, *args):
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return

        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(
            ChangeDeathFail(character_id=char_id, amount=1)
        )


class CHDeathSuccesses(ProgressiveIcon, ListenForStateChanges, TouchableMixin):
    current_death_successes: int = NumericProperty(0)
    max_death_successes: int = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=2 / 3,
            box_height=self.box_height,
            source=Resources.DEATH_SUCCESS,
            stacked=True,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="green",
            orientation="horizontal",
        )
        self.touch_init()
        self.listener_init()

        self.bind(
            current_death_successes=self.update_successes,
            max_death_successes=self.update_successes
        )

    def update_successes(self, *args):
        self.current_value = self.current_death_successes
        self.maximum_value = self.max_death_successes

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.current_death_successes = 0
            self.max_death_successes = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            current: Status = char.current_life
            maxi: Status = char.max_life

            # Invert again - we want what we've done,
            # not what we have left

            self.current_death_successes = maxi.death_successes - current.death_successes
            self.max_death_successes = maxi.death_successes

    def on_left_click(self, *args):
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return

        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(
            ChangeDeathSuccess(character_id=char_id, amount=-1)
        )

    def on_right_click(self, *args):
        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return

        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(
            ChangeDeathSuccess(character_id=char_id, amount=1)
        )


class CHDeathKnockedOut(ProgressiveIcon, ListenForStateChanges, TouchableMixin):
    current_hp: int = NumericProperty(1)
    max_hp: int = NumericProperty(1)
    stabilized: bool = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=2 / 3,
            box_height=self.box_height,
            source=Resources.DEATH_ICON,
            stacked=False,
            current_value=0,
            maximum_value=1,
            pr_empty_color="black",
            pr_full_color="red",
            orientation="horizontal",
        )
        self.touch_init()
        self.listener_init()

        self.bind(
            current_hp=self.hp_updated,
            max_hp=self.hp_updated,
            stabilized=self.hp_updated
        )

    def hp_updated(self, *args):
        self.current_value = 1 if self.current_hp <= 0 else 0
        if self.stabilized:
            self.pr_full_color = "darkgreen"
        else:
            self.pr_full_color = "red"
        self.tooltip_text = help_generator.death(self.max_hp)

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.current_hp = 1
            self.max_hp = 1
            self.stabilized = False
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            current: Status = char.current_life
            maxi: Status = char.max_life

            self.current_hp = current.HP
            self.max_hp = maxi.HP

            # If we don't need to get any more successes, we're
            # stabilized.
            self.stabilized = current.death_successes == 0

    def on_left_click(self, position):
        super().on_left_click(position)

        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return

        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(DeathSave(character_id=char_id))


class CHDeathSaves(MDBoxLayout, BoxSized, ListenForStateChanges):
    """
    Death Throw successes + failures
    """
    def __init__(self, **kwargs):
        super().__init__(box_width=2, box_height=1, **kwargs)
        self.box_init()
        self.listener_init()

        self.failures = CHDeathFails()
        self.successes = CHDeathSuccesses()
        self.knocked_out = CHDeathKnockedOut()

        self.add_widget(self.failures)
        self.add_widget(self.knocked_out)
        self.add_widget(self.successes)


class CHHitpoints(ProgressiveText, ListenForStateChanges, TouchableMixin):
    """
    Hitpoint heart
    """

    current_hp: int = NumericProperty(1)
    max_hp: int = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.HITPOINTS_ICON,
            pr_full_color="red",
            pr_empty_color="black",
            theme_text_color="Custom",
            text_color="white",
            current_value=0,
            maximum_value=1,
            box_width=2,
            box_height=2,
            tooltip_text=help_generator.HP(),
            **kwargs,
        )
        self.touch_init()
        self.listener_init()

        self.bind(current_hp=self.update_hp, max_hp=self.update_hp)

    def update_hp(self, *args):
        self.current_value = self.current_hp
        self.maximum_value = self.max_hp

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        # No reason to filter events, kivy will figure things out when we set properties

        # We might have changed the current character's icon. Look it up
        if state_manager.view_state.focused_character is None:
            self.current_hp = 1
            self.max_hp = 1
        else:
            char: Character = state_manager.game_state.characters[
                state_manager.view_state.focused_character]
            current: Status = char.current_life
            maxi: Status = char.max_life

            self.current_hp = current.HP
            self.max_hp = maxi.HP

    def on_left_click(self, pos):
        super().on_left_click(pos)

        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return

        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(ChangeHP(character_id=char_id, amount=-1))

    def on_right_click(self, pos):
        super().on_right_click(pos)

        if self.state_manager is None:
            return
        if self.state_manager.view_state.focused_character is None:
            return

        char_id: str = self.state_manager.view_state.focused_character
        self.state_manager.push_event(ChangeHP(character_id=char_id, amount=1))


class CHLife(MDBoxLayout, BoxSized, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical", box_width=2, box_height=3, **kwargs
        )
        self.box_init()
        self.listener_init()

        self.death_saves = CHDeathSaves()
        self.hitpoints = CHHitpoints()
        self.add_widget(self.hitpoints)
        self.add_widget(self.death_saves)
