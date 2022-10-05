"""
Game events actually impact game state
"""

from .ev_base import GameEvent, RollEvent, GameOrViewEvent
from dataclasses import dataclass
import typing as T

from ..character.character import Character
from ..character.active_effects import Debuffs, Buffs
from ..state.game_state import GameState
from ..state.view_state import ViewState
from ..dice.rolls import Roll, CompletedRoll
from ..dice.dice import Dice
from ..dice.advantage import RollStatus


@dataclass(frozen=True)
class ApplyEffectToCharacter(GameEvent):
    character_id: str = ""
    effect: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        assert self.effect.strip(), "Empty effect"
        char = g.characters[self.character_id]
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
        char = g.characters[self.character_id]
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
        char = g.characters[self.character_id]
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
        char = g.characters[self.character_id]
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
        char = g.characters[self.character_id]

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
        char = g.characters[self.character_id]

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
        char = g.characters[self.character_id]

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
        char = g.characters[self.character_id]

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
        char = g.characters[self.character_id]

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
        char = g.characters[self.character_id]

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
        char = g.characters[self.character_id]

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
        char = g.characters[self.character_id]

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
        char = g.characters[self.character_id]

        # Roll 1d2 to restore shields
        roll = Roll(faces=Dice.D2)
        completed = CompletedRoll.realize(roll)

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
        char = g.characters[self.character_id]

        # Reduce skinsuit power by however much we restored
        new_status = char.current_life.delta(shield_power=-1 * self.amount_restored)
        char.current_life = new_status



@dataclass(frozen=True)
class ChangeHP(GameEvent):
    character_id: str = ""
    amount: int = -1

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char = g.characters[self.character_id]

        hp_delta = self.amount

        # Account for hard to treat debuff (-1 to heals, no less than 1)
        if hp_delta > 1 and char.has_effect(Debuffs.HARD_TO_TREAT):
            hp_delta -= 1
    
        if hp_delta > 0:
            # This is a heal, clear out any death statuses
            death_fail_delta = char.max_life.death_fails
            death_success_delta = char.max_life.death_successes
        else:
            death_fail_delta=0
            death_success_delta=0

        new_status = char.current_life.delta(HP=hp_delta, death_fails=death_fail_delta, death_successes=death_success_delta, max_st=char.max_life)
        if char.current_life == new_status:
            # No damage .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            return ChangeHP(
                event_id=self.event_id,
                character_id=self.character_id,
                amount=new_status.HP - old_status.HP
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(HP=-1 * self.amount, max_st=char.max_life)
        char.current_life = new_status



@dataclass(frozen=True)
class ChangeDeathFail(GameEvent):
    character_id: str = ""
    amount: int = -1

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char = g.characters[self.character_id]

        fail_delta = self.amount
        if not char.current_life.HP <= 0:
            # I'm not KO'd.. Death fails aren't applicable
            # Regardless of what was asked, just restore all death fails
            fail_delta = char.max_life.death_fails

    
        new_status = char.current_life.delta(death_fails=fail_delta, max_st=char.max_life)
        if char.current_life == new_status:
            # No change .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            return ChangeDeathFail(
                event_id=self.event_id,
                character_id=self.character_id,
                amount=new_status.death_fails - old_status.death_fails
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char = g.characters[self.character_id]

        new_status = char.current_life.delta(death_fails=-1 * self.amount, max_st=char.max_life)
        char.current_life = new_status



@dataclass(frozen=True)
class ChangeDeathSuccess(GameEvent):
    character_id: str = ""
    amount: int = -1

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char = g.characters[self.character_id]

        success_delta = self.amount
        if not char.current_life.HP <= 0:
            # I'm not KO'd.. Death successes aren't applicable
            # Regardless of what was asked, just restore all death successes
            success_delta = char.max_life.death_successes

    
        new_status = char.current_life.delta(death_successes=success_delta, max_st=char.max_life)
        if char.current_life == new_status:
            # No change .. no-op
            return None
        else:
            old_status = char.current_life
            char.current_life = new_status

            return ChangeDeathSuccess(
                event_id=self.event_id,
                character_id=self.character_id,
                amount=new_status.death_successes - old_status.death_successes
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char = g.characters[self.character_id]

        new_status = char.current_life.delta(death_successes=-1 * self.amount, max_st=char.max_life)
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
        char = g.characters[self.character_id]

        if char.current_life.HP > 0:
            # Not knocked out
            return None

        if char.current_life.death_successes <= 0:
            # Stable, don't need death saves
            return None
        
        if char.current_life.death_fails <= 0:
            # Already dead
            return None

        roll = Roll(Dice.D20)
        completed = CompletedRoll.realize(roll)
        
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

        new_status = char.current_life.delta(HP=hp_delta, death_fails=death_fail_delta, death_successes=death_success_delta, max_st=char.max_life)
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
        char = g.characters[self.character_id]

        # Increase suit power by 1
        new_status = char.current_life.delta(
            HP=-1 * self._hp_delta,
            death_fails=-1 * self._fail_delta,
            death_successes=-1 * self._success_delta,
            max_st=char.max_life
        )
        char.current_life = new_status

