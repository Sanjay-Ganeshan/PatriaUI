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