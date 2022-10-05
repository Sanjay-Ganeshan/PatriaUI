from ..character.stats import Stat


def armor_rating(
    current_armor_rating: int,
    base_armor_rating: int,
) -> str:
    txt = (
        f"Your enemy must roll > {current_armor_rating}\n"
        f"(with modifiers) to hit you.\n"
        f"LClick - cast Reactive Armor. RClick - expire Reactive Armor"
    )
    if base_armor_rating != current_armor_rating:
        txt = txt + f"\n [Active effects changed this from {base_armor_rating}]"

    return txt


def suit(suit_power: int) -> str:
    return (
        f"Your suit has {suit_power} charges left. \n"
        f"Recharge 2 per short rest, or to full at a logistics facility. \n"
        f"Use 1 charge for:\n"
        f"Reactive Armor - +3 armor until next turn\n"
        f"Strength Enhancement - +4 strength until next turn\n"
        f"Electronic Warfare - An automatic success on a basic hacking check\n"
        f"Ballistic Calculation - Your next, non-disadvantage attack with your primary weapon has advantage"
    )


def shield(shield_power: int, shield_capacity: int) -> str:
    return (
        f"Your energy shield has {shield_power} power. \n"
        f"Your shield absorbs damage as temporary HP. \n"
        f"Recharges 1d2 (max {shield_capacity}) per turn when stationary."
    )


def death(max_hp: int) -> str:
    return (
        f"When dying, make 1d20 death saves. Fail <= 10, Success > 10.\n"
        f"At 2 failures, or on a critical failure, you die. \n"
        f"On 3 successes, you're stabilized (don't roll saves)\n"
        f"On critical success, revive with 1 HP.\n"
        f"Taking DMG < {max_hp} destabilizes you and adds a fail. \n"
        f"Taking DMG >= {max_hp} kills you."
    )


def HP() -> str:
    return "Your health. At 0 HP, you are dying."


def deflect(n_free_casts: int, max_free_casts: int, intelligence: int) -> str:
    return (
        f"Deflect (reaction) can either reflect a grenade to a point of your choosing,\n"
        f"or increase your armor rating for 1 incoming attack by your INT modifier ({intelligence})\n"
        f"You can cast Deflect for free INT ({max_free_casts}) times per long rest.\n"
        f"{n_free_casts} free casts left. Further casting will consume HP."
    )


def revive(current_revives: int, max_revives: int) -> str:
    return (
        f"Nanobot tech can save you from death (1+CON) {max_revives} times per long rest.\n"
        f"{current_revives} uses remaining."
    )

def hit_dice() -> str:
    return (
        f"During a short rest, you can spend hit dice to recover. Each heals 1d6.\n"
        f"They are restored during a long rest."
    )

def stat_description(which_stat: Stat, stat_value: int) -> str:
    if which_stat == Stat.STRENGTH:
        return "Your physical capability",
    if which_stat == Stat.DEXTERITY:
        return "Your overall deftness",
    if which_stat == Stat.CONSTITUTION:
        return "Your overall hardiness",
    if which_stat == Stat.INTELLIGENCE:
        return "Your knowledge and learned skills",
    if which_stat == Stat.WISDOM:
        return "Your acquired cleverness",
    if which_stat == Stat.PROFICIENCY_BONUS:
        return (
            f"If you are proficient in an action, add ({stat_value:+d})\n"
            f"If you are an expert add double that ({2*stat_value:+d})"
        )
