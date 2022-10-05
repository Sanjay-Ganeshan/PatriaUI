import typing as T

from ..new_models.character.proficiencies import Proficiency


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
        "INCINERATE": "flame.png",
        "ELECTROCUTE": "bolt.png",
        "FREEZE": "snowflake.png",
        "WARP": "portal.png",
        "DEFLECT": "deflect.png",
        "REPULSE": "repulse.png",
        "FEEDBACK": "feedback.png",
        "TELEKINESIS": "hand.png",
    }

    DICE_ICONS = {
        2: "d2.png",
        4: "d4.png",
        6: "d6.png",
        8: "d8.png",
        10: "d10.png",
        12: "d12.png",
        20: "d20.png",
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

