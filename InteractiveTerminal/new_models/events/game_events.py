"""
Game events actually impact game state
"""

from .ev_base import GameEvent, RollEvent, GameOrViewEvent
from dataclasses import dataclass
import typing as T

from ..character.character import Character
from ..state.game_state import GameState
from ..state.view_state import ViewState


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
        new_status = char.current_life.delta(
            armor_rating=-1 * self.armor_mod
        )
        char.current_life = new_status


@dataclass(frozen=True)
class DeathSave(RollEvent):
    pass


@dataclass(frozen=True)
class StatTest(RollEvent):
    pass


@dataclass(frozen=True)
class SkillTest(RollEvent):
    pass


@dataclass(frozen=True)
class ChangeHP(GameEvent):
    pass


@dataclass(frozen=True)
class ChangePower(GameEvent):
    pass


@dataclass(frozen=True)
class ChangeShield(GameEvent):
    pass


@dataclass(frozen=True)
class UseHitDice(GameEvent):
    pass


@dataclass(frozen=True)
class SkillTest(GameEvent):
    pass


@dataclass(frozen=True)
class SkillTest(GameEvent):
    pass
