def armor_rating(
    current_armor_rating: int,
    base_armor_rating: int,
) -> str:
    txt = (
        f"Your enemy must roll > {current_armor_rating}\n"
        f"(with modifiers) to hit you."
    )
    if base_armor_rating != current_armor_rating:
        txt = txt + f"\n [Active effects changed this from {base_armor_rating}]"
    
    return txt