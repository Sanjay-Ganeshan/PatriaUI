"""
Game events actually impact game state
"""

import typing as T
from dataclasses import dataclass

from ..character.active_effects import Debuffs
from ..character.character import Character
from ..character.proficiencies import Proficiency
from ..character.stats import Stat
from ..dice.advantage import RollStatus
from ..dice.dice import Dice
from ..dice.rolls import CompletedRoll, Roll
from ..state.game_state import GameState
from ..state.view_state import ViewState
from .ev_base import GameEvent, GameOrViewEvent, RollEvent


@dataclass(frozen=True)
class ApplyEffectToCharacter(GameEvent):
    character_id: str = ""
    effect: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        assert self.effect.strip(), "Empty effect"
        char: Character = g.characters[self.character_id]
        if char.has_effect(self.effect):
            # We're not actually adding it, so we don't want to undo it
            return None
        else:
            char.add_effect(self.effect)
            return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        assert self.effect.strip(), "Empty effect"
        char: Character = g.characters[self.character_id]
        assert char.has_effect(
            self.effect
        ), f"{char.nameplate.name} is not affected by {self.effect}"
        char.remove_effect(self.effect)


@dataclass(frozen=True)
class RemoveEffectFromCharacter(GameEvent):
    character_id: str = ""
    effect: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        assert self.effect.strip(), "Empty effect"
        char: Character = g.characters[self.character_id]
        if not char.has_effect(self.effect):
            # Don't have it, can't remove it
            return None
        else:
            char.remove_effect(self.effect)
            return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        assert self.effect.strip(), "Empty effect"
        char: Character = g.characters[self.character_id]
        assert not char.has_effect(
            self.effect
        ), f"{char.nameplate.name} is already affected by {self.effect}"
        char.add_effect(self.effect)


@dataclass(frozen=True)
class ConsumeSkinsuitCharge(GameEvent):
    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Reduce suit power by 1
        new_status = char.current_life.delta(suit_power=-1, max_st=char.max_life)
        if char.current_life == new_status:
            # No power .. no-op
            return None
        else:
            char.current_life = new_status
            return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(suit_power=1, max_st=char.max_life)
        char.current_life = new_status


@dataclass(frozen=True)
class RestoreSkinsuitCharge(GameEvent):
    character_id: str = ""
    amount_restored: int = 2

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Increase suit power by up to 2
        new_status = char.current_life.delta(
            suit_power=self.amount_restored, max_st=char.max_life
        )
        if char.current_life == new_status:
            # No change .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            # Populate the amount restored - otherwise if we overcap then undo,
            # we'll be at 1 less skinsuit charge
            return RestoreSkinsuitCharge(
                event_id=self.event_id,
                character_id=self.character_id,
                amount_restored=new_status.suit_power - old_status.suit_power,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Reduce skinsuit power by however much we restored
        new_status = char.current_life.delta(suit_power=-1 * self.amount_restored)
        char.current_life = new_status


@dataclass(frozen=True)
class ModifyArmorRating(GameEvent):
    character_id: str = ""
    armor_mod: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(armor_rating=self.armor_mod)
        if char.current_life == new_status:
            # No power .. no-op
            return None
        else:
            orig_status = char.current_life
            char.current_life = new_status

            # Armor rating can't go below 0 .. so make sure mod
            # is correctly stored
            return ModifyArmorRating(
                event_id=self.event_id,
                character_id=self.character_id,
                armor_mod=new_status.armor_rating - orig_status.armor_rating,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(armor_rating=-1 * self.armor_mod)
        char.current_life = new_status


@dataclass(frozen=True)
class ConsumeShield(GameEvent):
    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Reduce shield power by 1
        new_status = char.current_life.delta(shield_power=-1, max_st=char.max_life)
        if char.current_life == new_status:
            # No power .. no-op
            return None
        else:
            char.current_life = new_status
            return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(shield_power=1, max_st=char.max_life)
        char.current_life = new_status


@dataclass(frozen=True)
class RestoreShield(RollEvent):
    character_id: str = ""

    amount_restored: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Roll 1d2 to restore shields
        if self.roll is None:
            roll = Roll(faces=Dice.D2)
            completed = CompletedRoll.realize(roll)
        else:
            completed = self.roll

        new_status = char.current_life.delta(
            shield_power=completed.total(), max_st=char.max_life
        )
        if char.current_life == new_status:
            # No change .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            # Populate the amount restored - otherwise if we overcap then undo,
            # we'll be at 1 less charge
            return RestoreShield(
                event_id=self.event_id,
                character_id=self.character_id,
                amount_restored=new_status.shield_power - old_status.shield_power,
                roll=completed,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Reduce skinsuit power by however much we restored
        new_status = char.current_life.delta(shield_power=-1 * self.amount_restored)
        char.current_life = new_status


@dataclass(frozen=True)
class ChangeHP(GameEvent):
    character_id: str = ""
    amount: int = -1

    _death_fail_delta: int = 0
    _death_success_delta: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        hp_delta = self.amount

        # Account for hard to treat debuff (-1 to heals, no less than 1)
        if hp_delta > 1 and char.has_effect(Debuffs.HARD_TO_TREAT):
            hp_delta -= 1

        if hp_delta > 0:
            # This is a heal, clear out any death statuses
            death_fail_delta = char.max_life.death_fails
            death_success_delta = char.max_life.death_successes
        else:
            death_fail_delta = 0
            death_success_delta = 0

        new_status = char.current_life.delta(
            HP=hp_delta,
            death_fails=death_fail_delta,
            death_successes=death_success_delta,
            max_st=char.max_life,
        )
        if char.current_life == new_status:
            # No damage .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            return ChangeHP(
                event_id=self.event_id,
                character_id=self.character_id,
                amount=new_status.HP - old_status.HP,
                _death_fail_delta=new_status.death_fails - old_status.death_fails,
                _death_success_delta=new_status.death_successes
                - old_status.death_successes,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(
            HP=-1 * self.amount,
            death_fails=-1 * self._death_fail_delta,
            death_successes=-1 * self._death_success_delta,
            max_st=char.max_life,
        )
        char.current_life = new_status


@dataclass(frozen=True)
class ChangeDeathFail(GameEvent):
    character_id: str = ""
    amount: int = -1

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        fail_delta = self.amount
        if not char.current_life.HP <= 0:
            # I'm not KO'd.. Death fails aren't applicable
            # Regardless of what was asked, just restore all death fails
            fail_delta = char.max_life.death_fails

        new_status = char.current_life.delta(
            death_fails=fail_delta, max_st=char.max_life
        )
        if char.current_life == new_status:
            # No change .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            return ChangeDeathFail(
                event_id=self.event_id,
                character_id=self.character_id,
                amount=new_status.death_fails - old_status.death_fails,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(
            death_fails=-1 * self.amount, max_st=char.max_life
        )
        char.current_life = new_status


@dataclass(frozen=True)
class ChangeDeathSuccess(GameEvent):
    character_id: str = ""
    amount: int = -1

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        success_delta = self.amount
        if not char.current_life.HP <= 0:
            # I'm not KO'd.. Death successes aren't applicable
            # Regardless of what was asked, just restore all death successes
            success_delta = char.max_life.death_successes

        new_status = char.current_life.delta(
            death_successes=success_delta, max_st=char.max_life
        )
        if char.current_life == new_status:
            # No change .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            return ChangeDeathSuccess(
                event_id=self.event_id,
                character_id=self.character_id,
                amount=new_status.death_successes - old_status.death_successes,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(
            death_successes=-1 * self.amount, max_st=char.max_life
        )
        char.current_life = new_status


@dataclass(frozen=True)
class DeathSave(RollEvent):
    character_id: str = ""

    _fail_delta: int = 0
    _success_delta: int = 0
    _hp_delta: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if char.current_life.HP > 0:
            # Not knocked out
            return None

        if char.current_life.death_successes <= 0:
            # Stable, don't need death saves
            return None

        if char.current_life.death_fails <= 0:
            # Already dead
            return None

        if self.roll is None:
            roll = Roll(Dice.D20)
            completed = CompletedRoll.realize(roll)
        else:
            completed = self.roll

        death_success_delta = 0
        death_fail_delta = 0
        hp_delta = 0

        if completed.total() == 20:
            hp_delta = 1
            death_success_delta = char.max_life.death_successes
            death_fail_delta = char.max_life.death_fails
        elif completed.total() == 1:
            death_success_delta = char.max_life.death_successes
            death_fail_delta = char.current_life.death_fails
        elif completed.total() <= 10:
            # Failure
            death_fail_delta = -1
        else:
            # Success
            death_success_delta = -1

        new_status = char.current_life.delta(
            HP=hp_delta,
            death_fails=death_fail_delta,
            death_successes=death_success_delta,
            max_st=char.max_life,
        )
        if char.current_life == new_status:
            # No damage .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            return DeathSave(
                event_id=self.event_id,
                roll=completed,
                character_id=self.character_id,
                _fail_delta=new_status.death_fails - old_status.death_fails,
                _success_delta=new_status.death_successes - old_status.death_successes,
                _hp_delta=new_status.HP - old_status.HP,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(
            HP=-1 * self._hp_delta,
            death_fails=-1 * self._fail_delta,
            death_successes=-1 * self._success_delta,
            max_st=char.max_life,
        )
        char.current_life = new_status


@dataclass(frozen=True)
class CastDeflect(GameEvent):
    """
    Cast deflect .. correctly uses free deflects before HP
    """

    character_id: str = ""

    _hp_delta: int = 0
    _deflect_delta: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        hp_delta = 0
        deflect_delta = 0

        if char.current_life.deflects > 0:
            deflect_delta = -1
        else:
            hp_delta = -1

        new_status = char.current_life.delta(
            HP=hp_delta, deflects=deflect_delta, max_st=char.max_life
        )
        old_status = char.current_life

        if old_status == new_status:
            # No HP to burn
            return None
        else:
            return CastDeflect(
                event_id=self.event_id,
                character_id=self.character_id,
                _hp_delta=hp_delta,
                _deflect_delta=deflect_delta,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(
            HP=-1 * self._hp_delta,
            deflects=-1 * self._deflect_delta,
            max_st=char.max_life,
        )
        char.current_life = new_status


@dataclass(frozen=True)
class RestoreDeflect(GameEvent):
    """
    Refresh free deflect casts
    """

    character_id: str = ""

    _deflect_delta: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(
            deflects=char.max_life.deflects - char.current_life.deflects,
            max_st=char.max_life,
        )
        old_status = char.current_life

        if old_status == new_status:
            # No change
            return None
        else:
            return CastDeflect(
                event_id=self.event_id,
                character_id=self.character_id,
                _deflect_delta=new_status.deflects - old_status.deflects,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(
            deflects=-1 * self._deflect_delta,
            max_st=char.max_life,
        )
        char.current_life = new_status


@dataclass(frozen=True)
class ConsumeRevival(GameEvent):
    character_id: str = ""

    _hp_delta: int = 0
    _revive_delta: int = 0
    _death_fail_delta: int = 0
    _death_success_delta: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if char.current_life.HP > 0 or char.current_life.revives < 1:
            # Nothing to revive
            return None

        new_status = char.current_life.delta(
            revives=-1,
            death_fails=char.max_life.death_fails,
            death_successes=char.max_life.death_successes,
            HP=1,
            max_st=char.max_life,
        )
        old_status = char.current_life
        char.current_life = new_status
        return ConsumeRevival(
            event_id=self.event_id,
            character_id=self.character_id,
            _hp_delta=new_status.HP - old_status.HP,
            _revive_delta=new_status.revives - old_status.revives,
            _death_fail_delta=new_status.death_fails - old_status.death_fails,
            _death_success_delta=new_status.death_successes
            - old_status.death_successes,
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(
            revives=-1 * self._revive_delta,
            HP=-1 * self._hp_delta,
            death_fails=-1 * self._death_fail_delta,
            death_successes=-1 * self._death_success_delta,
            max_st=char.max_life,
        )
        char.current_life = new_status


@dataclass(frozen=True)
class RestoreRevival(GameEvent):
    """
    Restores a single revival to character_id
    """

    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(revives=1, max_st=char.max_life)
        if char.current_life == new_status:
            # No change .. no-op
            return None
        else:
            return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Reduce revives by however much we restored
        new_status = char.current_life.delta(revives=-1)
        char.current_life = new_status


@dataclass(frozen=True)
class RestoreHitDice(GameEvent):
    character_id: str = ""
    _hit_dice_restored: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(
            hit_dice=char.max_life.hit_dice, max_st=char.max_life
        )
        if char.current_life == new_status:
            # Already full .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status
            return RestoreHitDice(
                event_id=self.event_id,
                character_id=self.character_id,
                _hit_dice_restored=new_status.hit_dice - old_status.hit_dice,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(
            hit_dice=-1 * self._hit_dice_restored, max_st=char.max_life
        )
        char.current_life = new_status


@dataclass(frozen=True)
class UseHitDice(RollEvent):
    character_id: str = ""

    _hp_delta: int = 0
    _death_fail_delta: int = 0
    _death_success_delta: int = 0

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if char.current_life.hit_dice < 1 or char.current_life.HP >= char.max_life.HP:
            # No hit dice, or no need to heal
            return None

        if self.roll is None:
            # Roll 1d6 to restore HP
            roll = Roll(faces=Dice.D6)
            completed = CompletedRoll.realize(roll)
        else:
            completed = self.roll

        to_heal = completed.total()
        if to_heal > 1 and char.has_effect(Debuffs.HARD_TO_TREAT):
            to_heal -= 1

        new_status = char.current_life.delta(
            HP=to_heal,
            hit_dice=-1,
            death_fails=char.max_life.death_fails,
            death_successes=char.max_life.death_successes,
            max_st=char.max_life,
        )

        old_status = char.current_life
        char.current_life = new_status

        return UseHitDice(
            event_id=self.event_id,
            character_id=self.character_id,
            roll=completed,
            _hp_delta=new_status.HP - old_status.HP,
            _death_fail_delta=new_status.death_fails - old_status.death_fails,
            _death_success_delta=new_status.death_successes
            - old_status.death_successes,
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        new_status = char.current_life.delta(
            HP=-1 * self._hp_delta,
            hit_dice=1,
            death_fails=-1 * self._death_fail_delta,
            death_successes=-1 * self._death_success_delta,
            max_st=char.max_life,
        )
        char.current_life = new_status


@dataclass(frozen=True)
class StatOrSkillTest(RollEvent):
    character_id: str = ""
    stat_or_skill: T.Union[Stat, Proficiency] = Stat.PROFICIENCY_BONUS

    _prev_roll_status: T.Optional[RollStatus] = None

    def __post_init__(self):
        assert (
            self.stat_or_skill != Stat.PROFICIENCY_BONUS
        ), "Cannot roll in Proficiency - it must be a stat or skill"
        assert isinstance(self.stat_or_skill, (Stat, Proficiency))

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if self.roll is None:
            # Roll 1d6 to restore HP
            if isinstance(self.stat_or_skill, Stat):
                modifier = char.stat_block[self.stat_or_skill]
            elif isinstance(self.stat_or_skill, Proficiency):
                modifier = (
                    char.stat_block[self.stat_or_skill]
                    * char.stat_block[Stat.PROFICIENCY_BONUS]
                    + char.stat_block[self.stat_or_skill.corresponding_stat()]
                )

            roll = Roll(
                faces=Dice.D20,
                n_dice=1,
                modifier=modifier,
                status=char.next_roll_status,
            )

            # Clear the next roll status, save info for undo
            prev_roll_status = char.next_roll_status
            char.next_roll_status = RollStatus.STANDARD

            completed = CompletedRoll.realize(roll)
        else:
            prev_roll_status = None
            completed = self.roll

        return StatOrSkillTest(
            event_id=self.event_id,
            roll=completed,
            character_id=self.character_id,
            stat_or_skill=self.stat_or_skill,
            _prev_roll_status=prev_roll_status,
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if self._prev_roll_status is not None:
            char.next_roll_status = self._prev_roll_status
