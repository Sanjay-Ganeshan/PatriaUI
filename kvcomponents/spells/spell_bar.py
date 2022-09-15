from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout

from ...models.game import THE_GAME
from ...models.app_settings import BOX_HEIGHT, BOX_WIDTH
from ..shared.box_sized_mixin import BoxSized
from ..shared.touchable_mixin import TouchableMixin
from ..shared.tooltip import OptionalTooltip
from ..shared.needs_character_mixin import NeedsConstants
from ..resource_list import Resources
from kivy.properties import StringProperty

class SpellIcon(Image, BoxSized, NeedsConstants, TouchableMixin, OptionalTooltip):
    spell_name = StringProperty("INCINERATE")
    
    def __init__(self, **kwargs):
        super().__init__(
            source="",
            allow_stretch=True,
            **kwargs,
        )
        self.source = Resources.SPELLS[self.spell_name]
        self.box_init()
        self.constants_init()
        self.touch_init()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
    
    def _cast_spell(self):
        pass

    def on_left_click(self, position):
        super().on_left_click(position)
        current_character =  THE_GAME.get_current_character()
        if current_character.CURRENT_HP > 0:
            THE_GAME.adjust_current_character(
                CURRENT_HP=current_character.CURRENT_HP-1,
            )
            self._cast_spell()

class SpellIncinerate(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="INCINERATE",
            color="darkred",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        pass

class SpellElectrocute(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="ELECTROCUTE",
            color="yellow",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        pass

class SpellFreeze(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="FREEZE",
            color="lightblue",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        pass

class SpellWarp(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="WARP",
            color="magenta",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        pass

class SpellDeflect(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="DEFLECT",
            color="blue",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        pass

class SpellRepulse(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="REPULSE",
            color="darkorange",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        pass

class SpellFeedback(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="FEEDBACK",
            color="purple",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        pass

class SpellTelekinesis(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="TELEKINESIS",
            color="orange",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        pass

class SpellBar(BoxSized, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=2,
            orientation="horizontal",
        )
        self.box_init()

        self.spells = [
            SpellIncinerate(
                box_height=2,
                box_width=1.5,
            ),
            SpellElectrocute(
                box_height=2,
                box_width=1.5,
            ),
            SpellFreeze(
                box_height=2,
                box_width=1.5,
            ),
            SpellWarp(
                box_height=2,
                box_width=1.5,
            ),
            SpellDeflect(
                box_height=2,
                box_width=1.5,
            ),
            SpellRepulse(
                box_height=2,
                box_width=1.5,
            ),
            SpellFeedback(
                box_height=2,
                box_width=1.5,
            ),
            SpellTelekinesis(
                box_height=2,
                box_width=1.5,
            ),
        ]
        for each_spell in self.spells:
            self.add_widget(each_spell)
            
