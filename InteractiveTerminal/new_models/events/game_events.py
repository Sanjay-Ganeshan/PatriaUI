"""
Game events actually impact game state
"""

import typing as T
from dataclasses import dataclass, field

from ...utils import CircularList

from ..weapons.ammo_pack import AmmoPack

from ..character.active_effects import Debuffs
from ..character.character import Character
from ..character.proficiencies import Proficiency
from ..character.stats import Stat
from ..dice.advantage import RollStatus
from ..dice.dice import Dice, Critical
from ..dice.rolls import CompletedRoll, Roll
from ..state.game_state import GameState
from ..state.view_state import ViewState
from ..spells.spell_list import Spell
from ..weapons.weapon import Weapon
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
        new_status = char.current_life.delta(
            suit_power=-1, max_st=char.max_life
        )
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
        new_status = char.current_life.delta(
            suit_power=-1 * self.amount_restored
        )
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
        new_status = char.current_life.delta(
            shield_power=-1, max_st=char.max_life
        )
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
        new_status = char.current_life.delta(
            shield_power=1, max_st=char.max_life
        )
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
                amount_restored=new_status.shield_power -
                old_status.shield_power,
                roll=completed,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Reduce skinsuit power by however much we restored
        new_status = char.current_life.delta(
            shield_power=-1 * self.amount_restored
        )
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
                _death_fail_delta=new_status.death_fails -
                old_status.death_fails,
                _death_success_delta=new_status.death_successes -
                old_status.death_successes,
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

        crit = completed.is_critical()
        if crit == Critical.SUCCESS:
            hp_delta = 1
            death_success_delta = char.max_life.death_successes
            death_fail_delta = char.max_life.death_fails
            chat_msg = f"{char.nameplate.name} rolls a death save.{crit.msg()} {char.nameplate.she.capitalize()} is back up!"
        elif completed.total() == 1:
            death_success_delta = char.max_life.death_successes
            death_fail_delta = char.current_life.death_fails
            chat_msg = f"{char.nameplate.name} rolls a death save.{crit.msg()} {char.nameplate.she.capitalize()} is DEAD!"
        elif completed.total() <= 10:
            # Failure
            death_fail_delta = -1
            flavor = "Death looms closer." if char.current_life.death_fails > 1 else f"Death claims {char.nameplate.her}."
            chat_msg = f"{char.nameplate.name} fails a death save ({completed.total()}). {flavor}"
        else:
            # Success
            death_success_delta = -1
            chat_msg = f"{char.nameplate.name} passes a death save ({completed.total()}). {char.nameplate.her.capitalize()} breathing eases."

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
            g.chat_log.append(chat_msg)

            return DeathSave(
                event_id=self.event_id,
                roll=completed,
                character_id=self.character_id,
                _fail_delta=new_status.death_fails - old_status.death_fails,
                _success_delta=new_status.death_successes -
                old_status.death_successes,
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
        g.chat_log.pop()


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
            char.current_life = new_status
            g.chat_log.append(
                f"{char.nameplate.name} casts DEFLECT. As a reaction, she "
                f"can reflect a grenade, OR\n"
                f"increase her armor rating by {char.stat_block[Stat.INTELLIGENCE]} for a single incoming attack"
            )
            return CastDeflect(
                event_id=self.event_id,
                character_id=self.character_id,
                _hp_delta=new_status.HP - old_status.HP,
                _deflect_delta=new_status.deflects - old_status.deflects,
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
        g.chat_log.pop()


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
            char.current_life = new_status
            return RestoreDeflect(
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
            _death_success_delta=new_status.death_successes -
            old_status.death_successes,
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
            _death_success_delta=new_status.death_successes -
            old_status.death_successes,
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
                    char.stat_block[self.stat_or_skill] *
                    char.stat_block[Stat.PROFICIENCY_BONUS] +
                    char.stat_block[self.stat_or_skill.corresponding_stat()]
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

        chat_msg = (
            f"{char.nameplate.name} tests {self.stat_or_skill.value}. {completed.total()}!"
            f"{completed.is_critical().msg()}\n"
            f"{completed}"
        )

        g.chat_log.append(chat_msg)

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

        # We added this, so it won't be length 0
        g.chat_log.pop()


@dataclass(frozen=True)
class RandomRoll(RollEvent):
    character_id: str = ""
    faces: Dice = Dice.D20

    _prev_roll_status: T.Optional[RollStatus] = None

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if self.roll is None:
            roll = Roll(
                faces=self.faces,
                n_dice=1,
                modifier=0,
                status=char.next_roll_status,
            )

            # Clear the next roll status, save info for undo
            prev_roll_status = char.next_roll_status
            char.next_roll_status = RollStatus.STANDARD

            completed = CompletedRoll.realize(roll)
        else:
            prev_roll_status = None
            completed = self.roll

        chat_msg = (
            f"{char.nameplate.name} rolls a D{self.faces}. {completed.total()}!"
            f"{completed.is_critical().msg()}\n"
            f"{completed}"
        )

        g.chat_log.append(chat_msg)

        return RandomRoll(
            event_id=self.event_id,
            roll=completed,
            character_id=self.character_id,
            faces=self.faces,
            _prev_roll_status=prev_roll_status,
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if self._prev_roll_status is not None:
            char.next_roll_status = self._prev_roll_status

        # We added this, so it won't be length 0
        g.chat_log.pop()


@dataclass(frozen=True)
class ToggleAdvantage(GameEvent):
    character_id: str = ""

    _prev_roll_status: RollStatus = RollStatus.STANDARD

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        prev_roll_status = char.next_roll_status

        if char.next_roll_status == RollStatus.STANDARD:
            char.next_roll_status = RollStatus.ADVANTAGE
        elif char.next_roll_status == RollStatus.ADVANTAGE:
            char.next_roll_status = RollStatus.STANDARD
        elif char.next_roll_status == RollStatus.DISADVANTAGE:
            char.next_roll_status = RollStatus.ADVANTAGE

        return ToggleAdvantage(
            event_id=self.event_id,
            character_id=self.character_id,
            _prev_roll_status=prev_roll_status,
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        char.next_roll_status = self._prev_roll_status


@dataclass(frozen=True)
class ToggleDisadvantage(GameEvent):
    character_id: str = ""

    _prev_roll_status: RollStatus = RollStatus.STANDARD

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        prev_roll_status = char.next_roll_status

        if char.next_roll_status == RollStatus.STANDARD:
            char.next_roll_status = RollStatus.DISADVANTAGE
        elif char.next_roll_status == RollStatus.ADVANTAGE:
            char.next_roll_status = RollStatus.DISADVANTAGE
        elif char.next_roll_status == RollStatus.DISADVANTAGE:
            char.next_roll_status = RollStatus.STANDARD

        return ToggleDisadvantage(
            event_id=self.event_id,
            character_id=self.character_id,
            _prev_roll_status=prev_roll_status,
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        char.next_roll_status = self._prev_roll_status


@dataclass(frozen=True)
class CastSpell(GameEvent):
    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if char.current_life.HP <= 0:
            return None
        else:
            char.current_life = char.current_life.delta(HP=-1)
            return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Restore the HP used to cast
        new_status = char.current_life.delta(
            HP=1,
            max_st=char.max_life,
        )
        char.current_life = new_status


@dataclass(frozen=True)
class SpellAttack(RollEvent):
    """
    Cast any spell attack.
    Spell attacks pit D20+INT+Proficiency against the
    enemy's armor rating.
    """

    character_id: str = ""
    which_spell: Spell = Spell.INCINERATE

    _prev_roll_status: T.Optional[RollStatus] = None

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        old_status = char.current_life
        # Continue with spellcasting
        if self.roll is None:
            roll = Roll(
                faces=Dice.D20,
                n_dice=1,
                modifier=char.stat_block[Stat.INTELLIGENCE] +
                char.stat_block[Stat.PROFICIENCY_BONUS],
                status=char.next_roll_status,
            )

            # Clear the next roll status, save info for undo
            prev_roll_status = char.next_roll_status
            char.next_roll_status = RollStatus.STANDARD

            completed = CompletedRoll.realize(roll)
        else:
            prev_roll_status = None
            completed = self.roll

        chat_message = (
            f"{char.nameplate.name} attacks with {self.which_spell.value}. "
            f"{completed.total()} to hit.{completed.is_critical().msg()}\n"
            f"{completed}\n"
            f"(RClick for damage)"
        )

        g.chat_log.append(chat_message)
        return SpellAttack(
            event_id=self.event_id,
            roll=completed,
            character_id=self.character_id,
            which_spell=self.which_spell,
            _prev_roll_status=prev_roll_status
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Restore the HP used to cast
        if self._prev_roll_status:
            char.next_roll_status = self._prev_roll_status
        g.chat_log.pop()


@dataclass(frozen=True)
class SpellDamage(RollEvent):
    """
    Incinerate deals 3d10 on hit
    Electrocute deals 3d12 on hit and prevents enemy reactions.
    Repulse deals 3d8 on hit, and with a spell DC (11+INT+Proficiency)

    """

    character_id: str = ""

    _prev_roll_status: T.Optional[RollStatus] = None

    which_dice: Dice = field(default=Dice.D6, metadata={"IGNORESAVE": True})
    which_spell: Spell = field(
        default=Spell.INCINERATE, metadata={"IGNORESAVE": True}
    )
    enemy_save: T.Optional[Stat] = field(
        default=None, metadata={"IGNORESAVE": True}
    )
    effective_range: str = field(default="10m", metadata={"IGNORESAVE": True})

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if self.roll is None:
            roll = Roll(
                faces=self.which_dice,
                n_dice=3,
                status=char.next_roll_status,
            )

            # Clear the next roll status, save info for undo
            prev_roll_status = char.next_roll_status
            char.next_roll_status = RollStatus.STANDARD

            completed = CompletedRoll.realize(roll)
        else:
            prev_roll_status = None
            completed = self.roll

        chat_message = (
            f"{char.nameplate.name} deals {self.which_spell.value} damage (range: {self.effective_range}).\n"
        )

        if self.enemy_save is None:
            chat_message += self.get_effect(char, completed, None) + "\n"
        else:
            spell_save_dc = 11 + char.stat_block[
                Stat.PROFICIENCY_BONUS] + char.stat_block[Stat.INTELLIGENCE]
            chat_message += (
                f"The enemy must make {self.enemy_save.a_or_an()} {self.enemy_save.value[:3]} save (DC {spell_save_dc}).\n"
            )
            common_effect = self.get_effect(char, completed, None)
            if common_effect is not None:
                chat_message += common_effect + "\n"
            chat_message += "FAIL: " + self.get_effect(
                char, completed, False
            ) + "\n"
            chat_message += "PASS: " + self.get_effect(
                char, completed, True
            ) + "\n"

        chat_message += f"{completed}"

        g.chat_log.append(chat_message)
        return SpellDamage(
            event_id=self.event_id,
            roll=completed,
            character_id=self.character_id,
            which_dice=self.which_dice,
            which_spell=self.which_spell,
            enemy_save=self.enemy_save,
            effective_range=self.effective_range,
            _prev_roll_status=prev_roll_status
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if self._prev_roll_status is not None:
            char.next_roll_status = self._prev_roll_status

        g.chat_log.pop()

    def get_effect(
        self, char: Character, roll: CompletedRoll, save_pass: T.Optional[bool]
    ) -> T.Optional[str]:
        raise NotImplementedError()


class IncinerateDamage(SpellDamage):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **kwargs,
            which_dice=Dice.D10,
            which_spell=Spell.INCINERATE,
            enemy_save=None,
            effective_range="10m",
        )

    def get_effect(
        self, char: Character, roll: CompletedRoll, save_pass: T.Optional[bool]
    ) -> T.Optional[str]:
        return f"{char.nameplate.her.capitalize()} target takes {roll.total()} damage"


class ElectrocuteDamage(SpellDamage):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **kwargs,
            which_dice=Dice.D12,
            which_spell=Spell.ELECTROCUTE,
            enemy_save=None,
            effective_range="melee",
        )

    def get_effect(
        self, char: Character, roll: CompletedRoll, save_pass: T.Optional[bool]
    ) -> T.Optional[str]:
        return (
            f"{char.nameplate.her.capitalize()} target takes {roll.total()} damage "
            f"AND cannot make reactions until the end of {char.nameplate.name}'s next turn."
        )


class FreezeDamage(SpellDamage):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **kwargs,
            which_dice=Dice.D6,
            which_spell=Spell.FREEZE,
            enemy_save=Stat.CONSTITUTION,
            effective_range="16m",
        )

    def get_effect(
        self, char: Character, roll: CompletedRoll, save_pass: T.Optional[bool]
    ) -> T.Optional[str]:
        if save_pass is True:
            return "No effect."
        elif save_pass is False:
            return (
                f"Target takes {roll.total()} damage and their next roll is at disadvantage (Attack / Save / Ability)"
            )
        else:
            return None


class WarpDamage(SpellDamage):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **kwargs,
            which_dice=Dice.D8,
            which_spell=Spell.WARP,
            enemy_save=Stat.DEXTERITY,
            effective_range="12m, 4m AoE",
        )

    def get_effect(
        self, char: Character, roll: CompletedRoll, save_pass: T.Optional[bool]
    ) -> T.Optional[str]:
        if save_pass is True:
            return f"Target(s) take {(roll.total() + 1) // 2} damage."
        elif save_pass is False:
            return (f"Target(s) takes {roll.total()} damage.")
        else:
            return f"(Targets in AoE roll saves independently)"


class RepulseDamage(SpellDamage):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **kwargs,
            which_dice=Dice.D8,
            which_spell=Spell.WARP,
            enemy_save=Stat.STRENGTH,
            effective_range="melee",
        )

    def get_effect(
        self, char: Character, roll: CompletedRoll, save_pass: T.Optional[bool]
    ) -> T.Optional[str]:
        if save_pass is True:
            return (f"Target is knocked prone")
        elif save_pass is False:
            return f"Target is knocked up to 10m away. (May take fall / collision damage)"
        else:
            return f"Always: Target takes {roll.total()} damage"


class FeedbackDamage(SpellDamage):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            **kwargs,
            which_dice=Dice.D8,
            which_spell=Spell.FEEDBACK,
            enemy_save=Stat.WISDOM,
            effective_range="12m",
        )

    def get_effect(
        self, char: Character, roll: CompletedRoll, save_pass: T.Optional[bool]
    ) -> T.Optional[str]:
        if save_pass is True:
            return (f"{(roll.total() + 1) // 2} damage.")
        elif save_pass is False:
            return f"{roll.total()} damage."
        else:
            return f"(Effectiveness is halved without line of sight)"


@dataclass(frozen=True)
class CastTelekinesis(GameEvent):
    """
    Cast telekinesis
    """

    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if char.current_life.HP <= 0:
            return None
        else:
            char.current_life = char.current_life.delta(HP=-1)

            chat_message = (
                f"{char.nameplate.name} casts {Spell.TELEKINESIS.value}. \n"
                f"{char.nameplate.she.capitalize()} can move a small object within 10m "
                f"to another point within 10m of {char.nameplate.her}."
            )

            g.chat_log.append(chat_message)
            return CastTelekinesis(
                event_id=self.event_id,
                character_id=self.character_id,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        # Restore the HP used to cast
        new_status = char.current_life.delta(
            HP=1,
            max_st=char.max_life,
        )
        char.current_life = new_status
        g.chat_log.pop()


@dataclass(frozen=True)
class FireCurrentWeapon(GameEvent):
    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon: T.Optional[Weapon] = char.weapons.get()

        if weapon is None:
            return None

        fired: bool = weapon.fire()
        if not fired:
            return None
        else:
            return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon: T.Optional[Weapon] = char.weapons.get()

        assert weapon is not None, f"{char.nameplate.name} does not have a weapon equipped"

        weapon.undo_fire()


@dataclass(frozen=True)
class ChangeWeapons(GameEvent):
    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        char.weapons = char.weapons.next()

        return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        char.weapons = char.weapons.prev()


@dataclass(frozen=True)
class ChangeWeaponMode(GameEvent):
    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon: T.Optional[Weapon] = char.weapons.get()

        if weapon is None:
            return None
        else:
            weapon.next_mode()
            return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon = char.weapons.get()
        assert weapon is not None, f"{char.nameplate.name} does not have a weapon"
        weapon.prev_mode()


@dataclass(frozen=True)
class ChangeWeaponBurst(GameEvent):
    character_id: str = ""

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon: T.Optional[Weapon] = char.weapons.get()

        if weapon is None:
            return None
        else:
            if not weapon.next_burst():
                return None
            else:
                return self

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon = char.weapons.get()
        assert weapon is not None, f"{char.nameplate.name} does not have a weapon"
        weapon.prev_burst()


@dataclass(frozen=True)
class ChangeWeaponAmmo(GameEvent):
    character_id: str = ""

    _prev_clip_current: T.Optional[int] = None

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon: T.Optional[Weapon] = char.weapons.get()

        if weapon is None:
            return None
        else:
            prev_clip_current = weapon.clip_current
            if not weapon.switch_ammo():
                return None
            else:
                return ChangeWeaponAmmo(
                    event_id=self.event_id,
                    character_id=self.character_id,
                    _prev_clip_current=prev_clip_current,
                )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon = char.weapons.get()
        assert weapon is not None, f"{char.nameplate.name} does not have a weapon"
        if self._prev_clip_current is not None:
            weapon.undo_switch_ammo(self._prev_clip_current)


@dataclass(frozen=True)
class ReloadCurrentWeapon(GameEvent):
    character_id: str = ""

    _prev_clip_current: T.Optional[int] = None

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon: T.Optional[Weapon] = char.weapons.get()

        if weapon is None:
            return None
        else:
            prev_clip_current = weapon.clip_current
            if not weapon.reload():
                return None
            else:
                return ReloadCurrentWeapon(
                    event_id=self.event_id,
                    character_id=self.character_id,
                    _prev_clip_current=prev_clip_current,
                )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon = char.weapons.get()
        assert weapon is not None, f"{char.nameplate.name} does not have a weapon"
        if self._prev_clip_current is not None:
            weapon.unload()
            weapon.load(self._prev_clip_current)


@dataclass(frozen=True)
class AttackOrDamageCurrentWeapon(RollEvent):
    character_id: str = ""
    is_attack: bool = True

    _prev_roll_status: T.Optional[RollStatus] = None

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon: T.Optional[Weapon] = char.weapons.get()

        if weapon is None:
            return None

        if self.roll is None:
            roll: Roll
            if self.is_attack:
                roll = weapon.attack(char.stat_block)
            else:
                roll = weapon.damage(char.stat_block)

            (next_roll, this_roll) = char.next_roll_status.apply(roll.status)

            if next_roll != char.next_roll_status:
                prev_roll_status = char.next_roll_status
                char.next_roll_status = next_roll
            else:
                prev_roll_status = None

            completed = CompletedRoll.realize(roll.replace(status=this_roll))

        else:
            prev_roll_status = None
            completed = self.roll

        chat_message: str

        if self.is_attack:
            chat_message = (
                f"{char.nameplate.name} attacks with {char.nameplate.her} {weapon.short_name}. "
                f"{completed.total()} to hit. {completed.is_critical().msg()}\n"
            )
        else:
            chat_message = (
                f"{char.nameplate.name} deals {completed.total()} damage with {char.nameplate.her} {weapon.short_name}\n"
            )

        ammo = weapon.ammo.get()
        needs_description: bool = False
        if ammo is not None:
            ammo_add = ammo.name
            needs_description = True
        else:
            ammo_add = ""

        mode = weapon.mode.get()
        if mode is not None:
            mode_add = f" mode: {mode}"
            needs_description = True
        else:
            mode_add = ""

        burst = weapon.burst.get()
        if burst is not None:
            burst_add = f"{burst}x"
            needs_description = True
        else:
            burst_add = ""

        if needs_description:
            description = f"[{burst_add}{ammo_add}{mode_add}]\n"
        else:
            description = ""

        chat_message += description
        added_effects = weapon.get_additional_effects(
            is_attack=self.is_attack, roll=completed
        )
        if added_effects is not None:
            chat_message += added_effects

        if completed.roll.n_dice > 0:
            chat_message += f"{completed}"

        g.chat_log.append(chat_message)

        return AttackOrDamageCurrentWeapon(
            event_id=self.event_id,
            is_attack=self.is_attack,
            roll=completed,
            character_id=self.character_id,
            _prev_roll_status=prev_roll_status,
        )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        if self._prev_roll_status is not None:
            char.next_roll_status = self._prev_roll_status

        g.chat_log.pop()


@dataclass(frozen=True)
class ResupplyWeapon(GameEvent):
    character_id: str = ""
    _prev_state: T.Dict[str, int] = field(default_factory=dict)

    def do(self, v: ViewState, g: GameState) -> T.Optional[GameOrViewEvent]:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon: T.Optional[Weapon] = char.weapons.get()

        if weapon is None:
            return None
        else:
            prev_state = weapon.restore()

            return ResupplyWeapon(
                event_id=self.event_id,
                character_id=self.character_id,
                _prev_state=prev_state,
            )

    def undo(self, v: ViewState, g: GameState) -> None:
        assert (
            self.character_id in g.characters
        ), f"Not a character: {self.character_id}"
        char: Character = g.characters[self.character_id]

        weapon = char.weapons.get()
        assert weapon is not None, "No weapon"
        weapon.undo_restore(self._prev_state)
