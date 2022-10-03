from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.core.image import Image as CImage
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.graphics import (
    Rectangle,
    Line,
    Color,
    InstructionGroup,
)

from ...models.location import Vector2

from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_map_mixin import NeedsMap
from ...models.app_settings import BOX_WIDTH
from ...models.map.maps import Map, MapLine, MapImage, MapLayer, TMapInstruction
import typing as T
import itertools

class MapDrawing(InstructionGroup):
    def __init__(
        self,
        the_map: Map,
        southwest_corner: Vector2,
        northeast_corner: Vector2,
        pos: Vector2,  # Bottom left origin
        size: Vector2,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.the_map: Map = the_map
        self.southwest_corner: Vector2 = southwest_corner
        self.northeast_corner: Vector2 = northeast_corner

        self.cached_textures = {}

        self.pos: Vector2 = pos
        self.size: Vector2 = size

        for each_layer in the_map.layers:
            for each_instruction in each_layer.instructions:
                self.draw(each_instruction)

    def _load_texture(self, tex_name: str) -> T.Optional[Texture]:
        if tex_name not in self.cached_textures:
            tex = CImage(f"images/maps/{tex_name}.png").texture
            self.cached_textures[tex_name] = tex

        return self.cached_textures.get(tex_name, None)

    def draw(self, ins: TMapInstruction) -> None:
        if isinstance(ins, MapImage):
            # First, add the tint
            self.add(Color(*ins.color))

            # Now, add the drawing rectangle
            bottom_left = self.point_to_screen(ins.southwest_corner)
            top_right = self.point_to_screen(ins.northeast_corner)

            rect_size = top_right - bottom_left


            rect = Rectangle(
                pos = bottom_left.tup(),
                size = rect_size.tup(),
                texture = self._load_texture(ins.map_id)
            )

            self.add(rect)
        elif isinstance(ins, MapLine):
            # First, add the color
            self.add(Color(*ins.color))
            # Then add the polyline
            self.add(
                Line(points=list(itertools.chain((
                    self.point_to_screen(p).tup() for p in ins.coords
                ))), width=ins.width)
            )
        else:
            raise NotImplementedError(f"Map can't draw type: {type(ins)} -- {ins}")

    def point_to_screen(self, point: Vector2) -> Vector2:
        return point.renorm(
            self.southwest_corner.x,
            self.northeast_corner.x,
            self.southwest_corner.y,
            self.northeast_corner.y,
            self.pos.x,
            self.pos.x + self.size.x,
            self.pos.y, # BOTTOM left is kivy, instead of top left
            self.pos.y + self.size.y,
        )


class MapView(Widget, BoxSized, NeedsMap):
    northeast_corner: ObjectProperty = ObjectProperty(Vector2.one())
    southwest_corner: ObjectProperty = ObjectProperty(Vector2.zero())

    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=10,
            **kwargs,
        )

        self.box_init()
        self.map_init()

        self.bind(
            pos=self.update,
            size=self.update,
        )


        self.ins_group: InstructionGroup = InstructionGroup()
        self.canvas.add(self.ins_group)


    def adapt_to_map(self, *args):
        super().adapt_to_map(*args)
        self.update()



    def update(self, *args):
        self.ins_group.clear()

        if self.the_map is not None:
            self.ins_group.add(MapDrawing(
                self.the_map,
                self.southwest_corner,
                self.northeast_corner,
                Vector2(*self.pos),
                Vector2(*self.size),
            ))
        


    def _get_background_tex_coords(self):
        return [
            # Bottom Left 
            0.0,
            1.0,

            # Bottom Right
            1.0,
            1.0,
            
            # Top Right
            1.0,
            0.0,

            # Top Left
            0.0,
            0.0,
        ]