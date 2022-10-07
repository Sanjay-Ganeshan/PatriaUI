import typing as T

from ..character.active_effects import Buffs
from ..spells.spell_list import Spell
from .ev_base import GameOrViewEvent
from .game_events import (ApplyEffectToCharacter, ConsumeSkinsuitCharge,
                          ModifyArmorRating, RemoveEffectFromCharacter, CastDeflect, SpellAttack,
                          CastTelekinesis, IncinerateDamage, FreezeDamage, ElectrocuteDamage, WarpDamage, RepulseDamage, FeedbackDamage)

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


def cast_spell(
    character_id: str,
    which_spell: Spell,
) -> T.List[GameOrViewEvent]:
    if which_spell == Spell.DEFLECT:
        return [CastDeflect(character_id=character_id)]
    elif which_spell in [
        Spell.INCINERATE,
        Spell.ELECTROCUTE,
        Spell.REPULSE,
    ]:
        return [SpellAttack(character_id=character_id, which_spell=which_spell)]
    elif which_spell == Spell.FREEZE:
        return [FreezeDamage(character_id=character_id)]
    elif which_spell == Spell.WARP:
        return [WarpDamage(character_id=character_id)]
    elif which_spell == Spell.FEEDBACK:
        return [FeedbackDamage(character_id=character_id)]
    elif which_spell == Spell.TELEKINESIS:
        return [CastTelekinesis(character_id=character_id)]
    else:
        raise NotImplementedError(f"Unexpected spell: {which_spell}")

def followup_spell(
    character_id: str,
    which_spell: Spell,
) -> T.List[GameOrViewEvent]:
    if which_spell == Spell.INCINERATE:
        return IncinerateDamage(character_id=character_id)
    elif which_spell == Spell.ELECTROCUTE:
        return ElectrocuteDamage(character_id=character_id)
    elif which_spell == Spell.REPULSE:
        return RepulseDamage(character_id=character_id)
    else:
        return []