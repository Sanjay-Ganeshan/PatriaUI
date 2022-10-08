from dataclasses import dataclass
import typing as T

@dataclass
class AmmoPack:
    name: str = "FMJ"
    current: int = 1
    capacity: int = 1

    def restore(self, n: T.Optional[int] = None) -> int:
        """
        Restore ammo to the pack. If n is provided,
        restores up to n (until capacity). If n is None,
        restores to full capacity.

        Returns the number of bullets restored.
        """
        if n is None:
            n = self.capacity
        n = min(self.capacity - self.current, n)
        self.current += n
        return n

    def can_consume(self, n: int) -> int:
        return self.current >= n

    def consume(self, n: int) -> int:
        """
        Consume up to n bullets. Return number consumed.
        """
        n = min(self.current, n)
        self.current -= n
        return n