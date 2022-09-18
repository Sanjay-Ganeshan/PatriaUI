from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout

from ...models.game import THE_GAME
from ...models.dice import Dice, roll
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

    def _roll_damage(self):
        pass

    def on_left_click(self, position):
        super().on_left_click(position)
        current_character =  THE_GAME.get_current_character()
        if current_character.CURRENT_HP > 0:
            THE_GAME.adjust_current_character(
                CURRENT_HP=current_character.CURRENT_HP-1,
            )
            self._cast_spell()

    def on_right_click(self, position):
        super().on_right_click(position)
        self._roll_damage()

class SpellIncinerate(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="INCINERATE",
            color="darkred",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        # Spell attack
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D20,
            modifier=char.S_PROFICIENCY_BONUS + char.S_INTELLIGENCE,
            description = f"{char.CHARACTER_NAME} attacks with INCINERATE (10m)",
            post_roll_desc = lambda total,raw:"(RClick for damage)"
        )
    
    def _roll_damage(self):
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D10,
            n_dice=3,
            description = f"{char.CHARACTER_NAME} rolls INCINERATE damage.",
            post_roll_desc=lambda total,raw: f"The enemy takes {total} fire damage"
        )

class SpellElectrocute(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="ELECTROCUTE",
            color="yellow",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        # Spell attack
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D20,
            modifier=char.S_PROFICIENCY_BONUS + char.S_INTELLIGENCE,
            description = f"{char.CHARACTER_NAME} attacks with ELECTROCUTE (melee)",
            post_roll_desc = lambda total,raw:"(RClick for damage)"
        )
    
    def _roll_damage(self):
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D12,
            n_dice=3,
            description = f"{char.CHARACTER_NAME} rolls ELECTROCUTE damage.",
            post_roll_desc=lambda total,raw: f"The enemy takes {total} electric damage, and can't take a reaction this turn."
        )

class SpellFreeze(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="FREEZE",
            color="lightblue",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        # Spell attack
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D6,
            n_dice=3,
            description = f"{char.CHARACTER_NAME} casts FREEZE. Enemy within 16m in LOS must make a CON save of {char.S_PROFICIENCY_BONUS + char.S_INTELLIGENCE + 11}",
            post_roll_desc = lambda total,raw:f"Success - nothing. Failure - Take {total} damage and disadvantage on next roll."
        )
    

class SpellWarp(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="WARP",
            color="magenta",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        # Spell attack
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D8,
            n_dice=3,
            description = f"{char.CHARACTER_NAME} casts WARP. Affected enemies (8m range, 4m AoE) must make a DEX save of {char.S_PROFICIENCY_BONUS + char.S_INTELLIGENCE + 11}",
            post_roll_desc = lambda total,raw:f"Success - {(total+1) // 2} damage. Failure - {total} damage."
        )

class SpellDeflect(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="DEFLECT",
            color="blue",
            **kwargs,
        )
    
    def on_left_click(self, position):
        current_character =  THE_GAME.get_current_character()
        if current_character.CURRENT_DEFLECTS > 0:
            THE_GAME.adjust_current_character(
                CURRENT_DEFLECTS=current_character.CURRENT_DEFLECTS-1,
            )
            self._cast_spell()

        elif current_character.CURRENT_HP > 0:
            THE_GAME.adjust_current_character(
                CURRENT_HP=current_character.CURRENT_HP-1,
            )
            self._cast_spell()

    def _cast_spell(self) -> None:
        # Spell attack
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D8,
            n_dice=3,
            description = f"{char.CHARACTER_NAME} casts DEFLECT. For this attack only, {char.PRONOUN_HER} armor is increased by {char.S_INTELLIGENCE}, or the grenade is reflected",
        )

class SpellRepulse(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="REPULSE",
            color="darkorange",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        # Spell attack
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D8,
            n_dice=3,
            description = f"{char.CHARACTER_NAME} casts REPULSE. Enemy (melee) must make a STR save of {char.S_PROFICIENCY_BONUS + char.S_INTELLIGENCE + 11}",
            post_roll_desc = lambda total,raw:f"Success - {total} damage and prone. Failure - {total} damage and sent flying 10m."
        )

class SpellFeedback(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="FEEDBACK",
            color="purple",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        char = THE_GAME.get_current_character()
        roll(
            faces=Dice.D8,
            n_dice=3,
            description = f"{char.CHARACTER_NAME} casts FEEDBACK. Enemy (12m) must make a WIS save of {char.S_PROFICIENCY_BONUS + char.S_INTELLIGENCE + 11}",
            post_roll_desc = lambda total,raw:f"Success - {(total+1)//2} damage. Failure - {total} damage and half movement speed for a turn. Deals half damage within LOS"
        )

class SpellTelekinesis(SpellIcon):
    def __init__(self, **kwargs):
        super().__init__(
            spell_name="TELEKINESIS",
            color="orange",
            **kwargs,
        )
    
    def _cast_spell(self) -> None:
        char = THE_GAME.get_current_character()
        THE_GAME.game_log.log(
            f"{char.CHARACTER_NAME} casts TELEKINESIS. She can move a small object from one point in a 10m radius to another."
        )

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
            
