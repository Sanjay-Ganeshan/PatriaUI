from dataclasses import dataclass, field
import typing as T
import math

from .character import Constants
from .dice import RollParams

class WeaponAttachment:
    def attach_to(self, weapon: "Weapon") -> None:
        return
    
    def modify_attack(
        self, 
        equipped_by: Constants,
        weapon: "Weapon",
        attack: RollParams
    ) -> RollParams:
        return attack
    
    def modify_damage(
        self, 
        equipped_by: Constants,
        weapon: "Weapon",
        damage: RollParams
    ) -> RollParams:
        return damage

@dataclass
class Weapon:
    name: str = "Project Lada Designated Marksman's Rifle"
    short_name: str = "Lada DMR"
    description: str = ""

    caliber: float = 7.8
    range_meters: int = 1200
    loaded_ammo: str = "Standard"
    ammo_count: T.Dict[str, T.Tuple[int, int]] = field(default_factory=lambda:{"Standard":0})
    clip_current: int = 0
    clip_capacity: int = 12
    mode: int = 0
    allowed_modes: T.List[str] = field(default_factory=lambda: ["default"])
    burst_size_ix: int = 0
    allowed_burst_sizes: T.List[int] = field(default_factory=lambda: [1])
    attachments: T.List["WeaponAttachment"] = field(default_factory=list)
    tags: T.Set[str] = field(default_factory=set)

    callbacks: T.List[T.Callable[["Weapon"], None]] = field(default_factory=list)

    def __post_init__(self) -> None:
        assert (
            len(self.allowed_modes) > 0
        ), f"Need at least 1 allowed mode [{self.name}]"
        assert 0 <= self.mode and self.mode < len(
            self.allowed_modes
        ), f"Mode out of range: {self.mode} [{self.name}]"
        assert self.loaded_ammo in self.ammo_count, (
            f"Invalid ammo: {self.loaded_ammo} for {self.name} .. expected "
            f"one of {self.ammo_count}"
        )

        assert 0 <= self.burst_size_ix and self.burst_size_ix < len(
            self.allowed_burst_sizes
        ), f"Burst IX out of range: {self.burst_size_ix} [{self.name}]"

        for each_attachment in self.attachments:
            each_attachment.attach_to(self)

    def notify_listeners(self) -> None:
        for each_callback in self.callbacks:
            each_callback(self)

    def bind(self, callback: T.Callable[["Weapon", None]]):
        self.callbacks.append(callback)

    def get_current_mode(self) -> str:
        return self.allowed_modes[self.mode]

    def get_ammo_types(self) -> T.List[str]:
        return sorted(self.ammo_count.keys())

    def replace_magazine(self, old: str, new: str) -> "Weapon":
        """
        Replaces one held magazine of OLD with NEW
        """
        cur_old, mx_old = self.ammo_count[old]
        self.ammo_count[old] = (cur_old - self.clip_capacity, mx_old - self.clip_capacity)

        cur_new, mx_new = self.ammo_count[new]
        self.ammo_count[new] = (cur_new + self.clip_capacity, mx_new + self.clip_capacity)
        
        return self

    def attack(self, equipped_by: Constants) -> RollParams:
        params = self._attack_impl(equipped_by)
        for each_attachment in self.attachments:
            params = each_attachment.modify_attack(
                equipped_by=equipped_by,
                weapon=self,
                attack=params,
            )
        
        n_rounds = self.allowed_burst_sizes[self.burst_size_ix]
        rounds_s = "rounds" if n_rounds > 1 else "round"
        params = params.replace(
            description=(
                f"{equipped_by.CHARACTER_NAME} fires "
                f"{n_rounds} {self.loaded_ammo} {rounds_s}"
            )
        )

        # Burst - add half of proficiency bonus, rounded up
        if n_rounds > 1:
            burst_bonus = math.ceil(equipped_by.S_PROFICIENCY_BONUS / 2)
            params = params.replace(
                modifier=params.modifier+burst_bonus,
            )
        return params

    def damage(self, equipped_by: Constants) -> RollParams:
        params = self._damage_impl(equipped_by)
        for each_attachment in self.attachments:
            params = each_attachment.modify_damage(
                equipped_by=equipped_by,
                weapon=self,
                damage=params,
            )
        return params

    def _attack_impl(self, equipped_by: Constants) -> RollParams:
        raise NotImplementedError(f"{self.name} in {self.mode} has no attack formula!")

    def _damage_impl(self, equipped_by: Constants) -> RollParams:
        raise NotImplementedError(f"{self.name} in {self.mode} has no damage formula!")

    def _increment_ammo(self, diff):
        cur, mx = self.ammo_count[self.loaded_ammo]
        self.ammo_count[self.loaded_ammo] = (cur + diff, mx)

    def _get_current_ammo(self) -> int:
        cur, mx = self.ammo_count[self.loaded_ammo]
        return cur

    def fire(self) -> bool:
        """
        Consumes ammo depending on burst size.
        Returns True iff we have enough ammo for the burst
        """
        if self.clip_current >= self.allowed_burst_sizes[self.burst_size_ix]:
            n_rounds = self.allowed_burst_sizes[self.burst_size_ix]
            self.clip_current -= n_rounds
            self._increment_ammo(-1 * n_rounds)
            self.notify_listeners()
            return True
        else:
            return False

    def reload(self) -> bool:
        """
        Reloads. Returns true if we had enough ammo and
        unfilled capacity to reload at least 1 bullet.
        """

        missing_in_clip: int = self.clip_capacity - self.clip_current
        remaining_of_type: int = self._get_current_ammo()

        amount_loaded = min(remaining_of_type, missing_in_clip)
        if amount_loaded <= 0:
            return False
        else:
            self._increment_ammo(amount_loaded)
            self.clip_current += amount_loaded
            self.notify_listeners()
            return True

    def switch_mode(self) -> str:
        prev_mode = self.mode
        self.mode += 1
        self.mode = self.mode % len(self.allowed_modes)
        if self.mode != prev_mode:
            self.notify_listeners()
        return self.allowed_modes[self.mode]

    def switch_burst(self) -> int:
        prev_burst = self.burst_size_ix
        self.burst_size_ix += 1
        self.burst_size_ix = self.burst_size_ix % len(self.allowed_burst_sizes)
        if self.burst_size_ix != prev_burst:
            self.notify_listeners()
        return self.allowed_burst_sizes[self.burst_size_ix]

    def switch_ammo(self) -> str:
        ammo_types=self.get_ammo_types()
        next_type = ammo_types[(ammo_types.index(self.loaded_ammo) + 1) % len(ammo_types)]
        if next_type != self.loaded_ammo:
            self.loaded_ammo = next_type
            self.notify_listeners()
        return self.loaded_ammo

    def add_attachment(self, attachment: WeaponAttachment) -> "Weapon":
        self.attachments.append(attachment)
        attachment.attach_to(self)
        return self