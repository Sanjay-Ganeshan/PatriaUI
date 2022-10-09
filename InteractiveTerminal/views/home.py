# The main page, regardless of contents
import random

from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout

from ..new_models.events.ev_base import GameOrViewEvent, RollEvent
from ..new_models.state.app_settings import BOX_HEIGHT, BOX_WIDTH, AppSettings
from ..new_models.state.state_manager import StateManager
from .page.body import Body
from .page.footer import Footer
from .page.header import Header
from .shared.box_sized_mixin import BoxSized
from .shared.listens_for_state_changes import ListenForStateChanges
from .sound_player import SoundPlayer
from ..new_models.dice.dice import Critical, Dice
from ..utils import get_username


class Home(MDBoxLayout, BoxSized, ListenForStateChanges):
    """
    The full screen's worth of content
    """
    def __init__(self, **kwargs):
        super().__init__(
            size_hint=(1.0, 1.0),
            box_width=BOX_WIDTH,
            box_height=BOX_HEIGHT,
            orientation="vertical",
            **kwargs,
        )
        self.box_init()
        self.listener_init()

        self.header = Header()
        self.body = Body()
        self.footer = Footer()

        self.add_widget(self.header)
        self.add_widget(self.body)
        self.add_widget(self.footer)

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, "text"
        )
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(
            on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up
        )

        Clock.schedule_interval(self.network_update, AppSettings.SecondsBetweenSync)


    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        if ev.username == get_username():
            if not is_forward:
                if SoundPlayer.keypress.state == "stop":
                    SoundPlayer.keypress.volume = 0.3
                    SoundPlayer.keypress.play()

            else:
                if isinstance(ev, RollEvent):
                    if all(
                        (d.state == "stop" for d in SoundPlayer.dice_rolls)
                    ) and SoundPlayer.coin_flip.state == "stop":
                        if ev.roll.roll.faces == Dice.D2:
                            r = SoundPlayer.coin_flip
                        else:
                            if ev.roll.is_critical() != Critical.NO:
                                r = SoundPlayer.dice_rolls[0]
                            else:
                                r = SoundPlayer.dice_rolls[random.randrange(
                                    1, len(SoundPlayer.dice_rolls)
                                )]
                        r.volume = 0.8
                        r.play()

    def _keyboard_closed(self):
        print("My keyboard have been closed!")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "h":
            AppSettings.TooltipsEnabled = not AppSettings.TooltipsEnabled
            # Return True to accept the key. Otherwise, it will be used by
            # the system.
            return True

        if keycode[1] == "z" and 'ctrl' in modifiers:
            # Return True to accept the key. Otherwise, it will be used by
            # the system.
            if self.state_manager is not None:
                self.state_manager.pop_event()
            return True

        # If we hit escape, release the keyboard
        if keycode[1] == "escape":
            keyboard.release()

        return False

    def _on_keyboard_up(self, keyboard, keycode):
        return False

    def network_update(self, dt) -> None:
        if self.state_manager is not None:
            self.state_manager.update_networked()