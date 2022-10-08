from dataclasses import dataclass
import typing as T


@dataclass(frozen=True)
class Vector2:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"

    def __add__(self, other: "Vector2") -> "Vector2":
        assert isinstance(other, Vector2), f"Cannot add {self} and {other}"
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        assert isinstance(other, Vector2), f"Cannot sub {self} and {other}"
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: "Vector2") -> "Vector2":
        assert isinstance(other, (float, int)), f"Cannot mul {self} and {other}"
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: "Vector2") -> "Vector2":
        assert isinstance(other, (float, int)), f"Cannot div {self} and {other}"
        return Vector2(self.x / other, self.y / other)

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    def normalized(self) -> "Vector2":
        return self / self.magnitude()

    @classmethod
    def zero(cls) -> "Vector2":
        return cls(0.0, 0.0)

    @classmethod
    def one(cls) -> "Vector2":
        return cls(1.0, 1.0)

    @classmethod
    def up(cls) -> "Vector2":
        return cls(0.0, 1.0)

    @classmethod
    def right(cls) -> "Vector2":
        return cls(1.0, 0.0)

    def renorm(
        self, oldMinX: float, oldMaxX: float, oldMinY: float, oldMaxY: float,
        newMinX: float, newMaxX: float, newMinY: float, newMaxY: float
    ) -> "Vector2":

        xNorm = (self.x - oldMinX) / (oldMaxX - oldMinX)
        yNorm = (self.y - oldMinY) / (oldMaxY - oldMinY)

        xNew = (xNorm * (newMaxX - newMinX)) + newMinX
        yNew = (yNorm * (newMaxY - newMinY)) + newMinY

        return Vector2(xNew, yNew)

    def tup(self) -> T.Tuple[int, int]:
        return int(self.x), int(self.y)
