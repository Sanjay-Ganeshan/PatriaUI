from ..shared.progressive_icon import ProgressiveText
from ..shared.box_sized_mixin import BoxSized
from ..shared.touchable_mixin import TouchableMixin
from ..shared.spacer import Spacer
from kivymd.uix.boxlayout import MDBoxLayout

from ..resource_list import Resources
from ...models.dice import Dice, RollStatus, roll
from ...models.game import THE_GAME
from ...models.app_settings import BOX_WIDTH


class AnyDiceRoller(ProgressiveText, TouchableMixin):
    def __init__(self, **kwargs):
        n_faces = kwargs.pop("maximum_value")
        super().__init__(
            source=Resources.DICE_ICONS[n_faces],
            current_value=n_faces,
            maximum_value=n_faces,
            pr_full_color="coral",
            box_width=1,
            box_height=1,
            bold=True,
            text_color="white",
            theme_text_color="Custom",
            **kwargs,
        )
        self.touch_init()
        self.bind(maximum_value=self.adjust_sides)
    
    def get_text(self) -> str:
        return str(self.maximum_value)
    
    def adjust_sides(self, *args):
        self.source = Resources.DICE_ICONS[self.maximum_value]
        self.current_value = self.maximum_value
    
    def on_left_click(self, *args):
        roll(Dice(self.maximum_value))


class DiceBar(MDBoxLayout, BoxSized):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=1,
            orientation="horizontal",
            **kwargs,
        )
        self.box_init()
        self.d2 = AnyDiceRoller(maximum_value=2)
        self.d4 = AnyDiceRoller(maximum_value=4)
        self.d6 = AnyDiceRoller(maximum_value=6)
        self.d8 = AnyDiceRoller(maximum_value=8)
        self.d10 = AnyDiceRoller(maximum_value=10)
        self.d12 = AnyDiceRoller(maximum_value=12)
        self.d20 = AnyDiceRoller(maximum_value=20)
        self.add_widget(Spacer(box_width=5, box_height=1))

        self.add_widget(self.d2)
        self.add_widget(self.d4)
        self.add_widget(self.d6)
        self.add_widget(self.d8)
        self.add_widget(self.d10)
        self.add_widget(self.d12)
        self.add_widget(self.d20)
    

        
