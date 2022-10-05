import typing as T

from ..character.active_effects import Buffs
from .ev_base import GameOrViewEvent
from .game_events import (ApplyEffectToCharacter, ConsumeSkinsuitCharge,
                          ModifyArmorRating, RemoveEffectFromCharacter)

# Some abilities as event chains

REACTIVE_ARMOR_BONUS = 3


def cast_reactive_armor(character_id: str) -> T.List[GameOrViewEvent]:
    # Can't double cast it, we keep track of the REACTIVE_ARMOR buff
    # Can't cast without consuming a skinsuit charge

    # Modify the armor rating if we newly added the effect AND
    # were able to consume a skinsuit charge

    # Chain will ensure all-or-nothing
    return [
        ApplyEffectToCharacter(
            character_id=character_id,
            effect=Buffs.REACTIVE_ARMOR.value,
        ),
        ConsumeSkinsuitCharge(character_id=character_id),
        ModifyArmorRating(character_id=character_id, armor_mod=REACTIVE_ARMOR_BONUS),
    ]


def expire_reactive_armor(character_id: str) -> T.List[GameOrViewEvent]:
    return [
        RemoveEffectFromCharacter(
            character_id=character_id, effect=Buffs.REACTIVE_ARMOR.value
        ),
        ModifyArmorRating(
            character_id=character_id, armor_mod=-1 * REACTIVE_ARMOR_BONUS
        ),
    ]
