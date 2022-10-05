import typing as T
from dataclasses import dataclass

@dataclass(frozen=True)
class Status:
    HP: int = 12
    armor_rating: int = 14
    revives: int = 1
    deflects: int = 1
    hit_dice: int = 2
    suit_power: int = 6
    shield_power: int = 2

    death_fails: int = 2
    death_successes: int = 3


    def delta(
        self,
        HP: int = 0,
        armor_rating: int = 0,
        revives: int = 0,
        deflects: int = 0,
        hit_dice: int = 0,
        suit_power: int = 0,
        shield_power: int = 0,
        death_fails: int = 0,
        death_successes: int = 0,
        max_st: T.Optional["Status"] = None,
    ) -> "Status":
        """
        Applies the given delta to each of the attributes,
        and returns a new Status with the modified values.

        Prevents anything from going below 0, and if "max_st"
        is provided, prevents anything from going above that max

        Returns the new status.
        """

        new_HP = max(0, self.HP + HP)
        new_armor_rating = max(0, self.armor_rating + armor_rating)
        new_revives = max(0, self.revives + revives)
        new_deflects = max(0, self.deflects + deflects)
        new_hit_dice = max(0, self.hit_dice + hit_dice)
        new_suit_power = max(0, self.suit_power + suit_power)
        new_shield_power = max(0, self.shield_power + shield_power)
        new_death_fails = max(0, self.death_fails + death_fails)
        new_death_successes = max(0, self.death_successes + death_successes)

        if max_st is not None:
            new_HP = min(new_HP, max_st.HP)
            new_armor_rating = min(new_armor_rating, max_st.armor_rating)
            new_revives = min(new_revives, max_st.revives)
            new_deflects = min(new_deflects, max_st.deflects)
            new_hit_dice = min(new_hit_dice, max_st.hit_dice)
            new_suit_power = min(new_suit_power, max_st.suit_power)
            new_shield_power = min(new_shield_power, max_st.shield_power)
            new_death_fails = min(new_death_fails, max_st.death_fails)
            new_death_successes = min(new_death_successes, max_st.death_successes)

        return Status(
            HP = new_HP,
            armor_rating = new_armor_rating,
            revives = new_revives,
            deflects = new_deflects,
            hit_dice = new_hit_dice,
            suit_power = new_suit_power,
            shield_power = new_shield_power,
            death_fails = new_death_fails,
            death_successes = new_death_successes,
        )