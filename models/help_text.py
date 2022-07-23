from .character import Constants
from .roll_status import RollStatus


class HelpText:
    def __init__(self, constants: Constants):
        self.ARMOR = (
            f"Your enemy must roll > {constants.ARMOR_RATING}\n"
            f"(with modifiers) to hit you."
        )

        self.SUIT = (
            f"Your suit has {constants.SUIT_POWER} charges left. \n"
            f"Recharge 2 per short rest, or to full at a logistics facility. \n"
            f"Use 1 charge for:\n"
            f"Reactive Armor - +3 armor until next turn\n"
            f"Strength Enhancement - +4 strength until next turn\n"
            f"Electronic Warfare - An automatic success on a basic hacking check\n"
            f"Ballistic Calculation - Your next, non-disadvantage attack with your primary weapon has advantage"
        )

        self.SHIELD = (
            f"Your energy shield has {constants.SHIELD_POWER} power. \n"
            f"Your shield absorbs damage as temporary HP. \n"
            f"Recharges 1d2 (max {constants.SHIELD_CAPACITY} per turn when stationary."
        )

        self.HP = f"Your health. At 0 HP, you are dying.\n"

        self.DEATH = (
            f"When dying, make 1d20 death saves. Fail <= 10, Success > 10.\n"
            f"At 2 failures, or on a critical failure, you die. \n"
            f"On 3 successes, you're stabilized (don't roll saves)\n"
            f"On critical success, revive with 1 HP.\n"
            f"Taking DMG < {constants.MAX_HP} destabilizes you and adds a fail. \n"
            f"Taking DMG >= {constants.MAX_HP} kills you."
        )

        self.DEFLECT = (
            f"You can cast Deflect for free INT ({constants.MAX_DEFLECTS}) times.\n"
            f"{constants.CURRENT_DEFLECTS} uses left. Refreshes on long rest."
        )

        self.REVIVAL = f"Nanobot tech can save you from death (1+CON) {constants.MAX_REVIVES} times per long rest.\n"

        self.HIT_DICE = (
            f"During a short rest, you can spend hit dice to recover. Each heals 1d6.\n"
            f"They are restored during a long rest."
        )

        self.STAT_DESCRIPTIONS = {
            "STRENGTH": "Your physical capability",
            "DEXTERITY": "Your overall deftness",
            "CONSTITUTION": "Your overall hardiness",
            "INTELLIGENCE": "Your knowledge and learned skills",
            "WISDOM": "Your acquired cleverness",
            "PROFICIENCY_BONUS": (
                f"If you are proficient in an action, add ({constants.S_PROFICIENCY_BONUS:+d})\n"
                f"If you are an expert add double that ({2*constants.S_PROFICIENCY_BONUS:+d})"
            ),
        }

        self.SKILL_DESCRIPTIONS = {
            # STR
            "STR_ATHLETICS": "FILLMEIN - ATHLETICS",
            "STR_COMBATIVES": "FILLMEIN - COMBATIVES",
            # DEX
            "DEX_ACROBATICS": "FILLMEIN - ACROBATICS",
            "DEX_STEALTH": "FILLMEIN - STEALTH",
            # INT
            "INT_INVESTIGATION": "FILLMEIN - INVESTIGATION",
            "INT_NATURE": "FILLMEIN - NATURE",
            "INT_ANIMAL_HANDLING": "FILLMEIN - ANIMAL_HANDLING",
            # WIS
            "WIS_INSIGHT": "FILLMEIN - INSIGHT",
            "WIS_MEDICINE": "FILLMEIN - MEDICINE",
            "WIS_PERCEPTION": "FILLMEIN - PERCEPTION",
            "WIS_SURVIVAL": "FILLMEIN - SURVIVAL",
            "WIS_SOCIAL": "FILLMEIN - SOCIAL",
        }

        self.ADVANTAGE = (
            (f"Your next roll is at {constants.NEXT_ROLL_STATUS.value}" if constants.NEXT_ROLL_STATUS != RollStatus.STANDARD else "") +
            (f"With advantage, you roll an extra die, drop the LOWEST roll.")
        )

        self.DISADVANTAGE = (
            (f"Your next roll is at {constants.NEXT_ROLL_STATUS.value}" if constants.NEXT_ROLL_STATUS != RollStatus.STANDARD else "") +
            (f"With disadvantage, you roll an extra die, drop the HIGHESt roll.")
        )

