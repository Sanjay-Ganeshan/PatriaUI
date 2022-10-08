from dataclasses import dataclass, field
import typing as T

from .location import Vector2


@dataclass
class MapLine:
    coords: T.List[Vector2] = field(default_factory=list)
    color: T.Tuple[float, float, float] = (0.0, 0.0, 0.0)
    width: int = 2


@dataclass
class MapImage:
    map_id: str = "example"  # Should have a matching images/maps/{map_id}.png
    color: T.Tuple[float, float, float] = (1.0, 1.0, 1.0)
    southwest_corner: Vector2 = Vector2.zero()
    northeast_corner: Vector2 = Vector2.one()


TMapInstruction = T.Union[MapLine, MapImage]


@dataclass
class MapLayer:
    instructions: T.List[TMapInstruction] = field(default_factory=list)


@dataclass
class Map:
    # All positions / distances in meters
    # South = -Y, North = +Y, West = -X, East = +X

    southwest_corner: Vector2 = Vector2.zero()
    northeast_corner: Vector2 = Vector2.one()

    layers: T.List[MapLayer] = field(default_factory=list)
