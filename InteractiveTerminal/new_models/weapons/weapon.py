from dataclasses import dataclass, field
import typing as T
import math

from ..character.stat_block import StatBlock
from ..character.stats import Stat
from ..dice.rolls import Roll, CompletedRoll
from ...utils import CircularList
from .ammo_pack import AmmoPack


@dataclass(frozen=True)
class WeaponAttachment:
    def get_name(self) -> str:
        return type(self).__name__

    def attach_to(self, weapon: "Weapon") -> None:
        return

    def modify_attack(
        self, equipped_by: StatBlock, weapon: "Weapon", attack: Roll
    ) -> Roll:
        return attack

    def modify_damage(
        self, equipped_by: StatBlock, weapon: "Weapon", damage: Roll
    ) -> Roll:
        return damage


@dataclass
class Weapon:
    name: str = field(default="<long name>", metadata={"IGNORESAVE": True})
    short_name: str = field(
        default="<short name>", metadata={"IGNORESAVE": True}
    )
    description: str = field(
        default="<description>", metadata={"IGNORESAVE": True}
    )

    caliber: T.Optional[float] = field(
        default=None, metadata={"IGNORESAVE": True}
    )
    range_meters: int = field(default=5, metadata={"IGNORESAVE": True})
    splash_meters: T.Optional[int] = field(
        default=None, metadata={"IGNORESAVE": True}
    )

    clip_capacity: int = 0
    clip_current: int = 1

    ammo: CircularList[AmmoPack] = field(default_factory=CircularList)
    mode: CircularList[str] = field(
        default_factory=lambda: CircularList(items=["Standard"])
    )
    burst: CircularList[int] = field(
        default_factory=lambda: CircularList(items=[1])
    )
    burst_improves_accuracy: bool = True
    attachments: T.List["WeaponAttachment"] = field(default_factory=list)
    tags: T.List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        for each_attachment in self.attachments:
            each_attachment.attach_to(self)

    def unload(self) -> None:
        """
        Unload the gun
        """
        self.clip_current = 0

    def load(self, n: T.Optional[int] = None) -> None:
        """
        Load the gun with active ammo. If n is provided, loads no more than
        n shots
        """
        if n is None:
            n = self.clip_capacity

        current_ammo_pack = self.ammo.get()
        if current_ammo_pack is None:
            self.clip_current = 0
        else:
            self.clip_current = min(
                current_ammo_pack.current, min(self.clip_capacity, n)
            )

    def replace_magazine(self, old: str, new: str) -> "Weapon":
        """
        Replaces one magazine of OLD with NEW, changing BOTH the max allowed
        and current.
        """
        old_pack = self.ammo.find(lambda pack: pack.name == old)
        new_pack = self.ammo.find(lambda pack: pack.name == new)

        assert old_pack is not None, f"Invalid ammo type: {old} for {self}"
        assert new_pack is not None, f"Invalid ammo type: {new} for {self}"

        ammo_transferred = min(old_pack.current, self.clip_capacity)
        capacity_transferred = min(old_pack.capacity, self.clip_capacity)

        new_pack.capacity += capacity_transferred
        new_pack.current += ammo_transferred
        old_pack.current -= ammo_transferred
        old_pack.capacity -= capacity_transferred
        return self

    def attack(self, equipped_by: StatBlock) -> Roll:
        params = self._attack_impl(equipped_by)
        for each_attachment in self.attachments:
            params = each_attachment.modify_attack(
                equipped_by=equipped_by,
                weapon=self,
                attack=params,
            )

        # Burst - add half of proficiency bonus, rounded up
        burst_size = self.burst.get()
        if burst_size is not None and burst_size > 1 and self.burst_improves_accuracy:
            burst_bonus = int((equipped_by[Stat.PROFICIENCY_BONUS] + 1) // 2)
            params = params.replace(modifier=params.modifier + burst_bonus, )
        return params

    def damage(self, equipped_by: StatBlock) -> Roll:
        params = self._damage_impl(equipped_by)
        for each_attachment in self.attachments:
            params = each_attachment.modify_damage(
                equipped_by=equipped_by,
                weapon=self,
                damage=params,
            )
        return params

    def _attack_impl(self, equipped_by: StatBlock) -> Roll:
        raise NotImplementedError(
            f"{self.name} in {self.mode} has no attack formula!"
        )

    def _damage_impl(self, equipped_by: StatBlock) -> Roll:
        raise NotImplementedError(
            f"{self.name} in {self.mode} has no damage formula!"
        )

    def fire(self) -> bool:
        """
        Consumes ammo depending on burst size.
        Returns True iff we have enough ammo for the burst
        """
        burst_size = self.burst.get() or 0
        if self.can_fire():
            self.ammo.get().consume(burst_size)
            self.clip_current -= burst_size
            return True
        else:
            return False

    def can_fire(self) -> bool:
        """
        Returns whether or not we can fire, but doesn't
        actually use ammo.
        """
        current_ammo = self.ammo.get()
        burst_size = self.burst.get() or 0

        if current_ammo is None:
            return False
        else:
            return current_ammo.can_consume(
                burst_size
            ) and self.clip_current >= burst_size

    def undo_fire(self) -> None:
        current_ammo = self.ammo.get()
        burst_size = self.burst.get() or 0
        if current_ammo is not None:
            current_ammo.restore(burst_size)
            self.clip_current += burst_size

    def reload(self) -> bool:
        """
        Reloads.
        """
        if self.clip_current == self.clip_capacity:
            return False
        else:
            self.unload()
            self.load()
            return True

    def next_mode(self) -> None:
        self.mode = self.mode.next()

    def prev_mode(self) -> None:
        self.mode = self.mode.prev()

    def next_burst(self) -> bool:
        if len(self.burst) <= 1:
            return False
        else:
            self.burst = self.burst.next()
            return True

    def prev_burst(self) -> None:
        self.burst = self.burst.prev()

    def switch_ammo(self) -> bool:
        if len(self.ammo) <= 1:
            return False
        else:
            self.unload()
            self.ammo = self.ammo.next()
            self.load()
            return True

    def undo_switch_ammo(self, prev_clip: int) -> None:
        self.unload()
        self.ammo = self.ammo.prev()
        self.lod(prev_clip)

    def add_attachment(self, attachment: WeaponAttachment) -> "Weapon":
        self.attachments.append(attachment)
        attachment.attach_to(self)
        return self

    def restore(self) -> T.Dict[str, int]:
        prev_state: T.Dict[str, int] = {}
        for each_pack in self.ammo:
            prev_state[each_pack.name] = each_pack.restore()
        return prev_state

    def undo_restore(self, prev_state: T.Dict[str, int]):
        for each_pack in self.ammo:
            if each_pack.name in prev_state:
                each_pack.consume(prev_state[each_pack.name])

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.pop(tag)

    def get_additional_effects(self, is_attack: bool,
                               roll: CompletedRoll) -> T.Optional[str]:
        return None
