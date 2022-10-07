import typing as T

from ..new_models.character.proficiencies import Proficiency
from ..new_models.dice.dice import Dice
from ..new_models.spells.spell_list import Spell


class Resources:
    ARMOR_ICON: str = "shield_white.png"

    MISSING: str = "missing.png"

    SKINSUIT_ICON: str = "suit.png"
    ENERGY_SHIELD_ICON: str = "shield_filled_white.png"

    HITPOINTS_ICON: str = "heart.png"

    DEATH_ICON: str = "skull.png"
    DEATH_FAIL: str = "cross.png"
    DEATH_SUCCESS: str = "check.png"

    DEFLECTION: str = "deflect.png"
    HIT_DICE: str = "heart.png"
    REVIVAL: str = "revival.png"

    STAT_ICON: str = "stat_triangle.png"
    PROFICIENCY_STAT_ICON: str = "proficiency_skill_tag.png"

    PROFICIENCY_MULTIPLIER_TO_SKILL_TAG: T.List[str] = [
        "skilltag_basic.png",
        "skilltag_prof.png",
        "skilltag_expert.png"
    ]

    SKILL_TO_ICON = {
        Proficiency.ATHLETICS: "athletics.png",
        Proficiency.COMBATIVES: "combatives.png",
        Proficiency.STEALTH: "stealth.png",
        Proficiency.ACROBATICS: "acrobatics.png",
        Proficiency.INVESTIGATION: "investigation.png",
        Proficiency.NATURE: "nature.png",
        Proficiency.ANIMAL_HANDLING: "horse.png",
        Proficiency.INSIGHT: "insight.png",
        Proficiency.MEDICINE: "medicine.png",
        Proficiency.PERCEPTION: "perception.png",
        Proficiency.SURVIVAL: "survival.png",
        Proficiency.SOCIAL: "social.png",
    }

    SPELLS = {
        Spell.INCINERATE: "flame.png",
        Spell.ELECTROCUTE: "bolt.png",
        Spell.FREEZE: "snowflake.png",
        Spell.WARP: "portal.png",
        Spell.DEFLECT: "deflect.png",
        Spell.REPULSE: "repulse.png",
        Spell.FEEDBACK: "feedback.png",
        Spell.TELEKINESIS: "hand.png",
    }

    SPELL_COLORS = {
        Spell.INCINERATE: "darkred",
        Spell.ELECTROCUTE: "yellow",
        Spell.FREEZE: "lightblue",
        Spell.WARP: "magenta",
        Spell.DEFLECT: "blue",
        Spell.REPULSE: "darkorange",
        Spell.FEEDBACK: "purple",
        Spell.TELEKINESIS: "orange",
    }

    DICE_ICONS = {
        Dice.D2: "d2.png",
        Dice.D4: "d4.png",
        Dice.D6: "d6.png",
        Dice.D8: "d8.png",
        Dice.D10: "d10.png",
        Dice.D12: "d12.png",
        Dice.D20: "d20.png",
    }

    ADVANTAGE = "advantage.png"
    DISADVANTAGE = "disadvantage.png"

    CYCLE = "cycle.png"

    WEAPON_ICONS = {
        "Lada DMR": "sniper.png",
        "Pistol": "pistol.png",
        "Splazer": "splaser.png",
        "Lada BR": "battle_rifle.png",
        "Lada CQ": "smg.png",
        "Vesna LSW": "lsw.png",
        "Grenade Launcher": "grenade_launcher.png",
        "Siren Knife": "knife.png",
        "Grenades": "grenade.png",
    }

    BULLET = "bullet.png"
    BULLET_LEFT = "bullet_left.png"
    BLOOD = "teardrop.png"
    RETICLE = "reticle.png"

    SFX_DICE_ROLL = ["diceroll.mp3", "diceroll2.mp3","diceroll3.mp3","diceroll4.mp3"]
    SFX_KEYPRESS = "keypress.mp3"
    SFX_COIN_FLIP = "coinflip.mp3"

