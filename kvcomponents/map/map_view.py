from kivy.uix.widget import Widget

from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import (
    InstructionGroup,
)

from ...models.location import Vector2

from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_map_mixin import NeedsMap
from .map_instruction import MapDrawing
import typing as T




class MapView(Widget, BoxSized, NeedsMap):
    map_center: ObjectProperty = ObjectProperty(Vector2.zero())
    map_scale: NumericProperty = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=10,
            box_height=10,
            **kwargs,
        )

        self.box_init()
        self.map_init()

        self.bind(
            pos=self.update,
            size=self.update,
            map_center=self.update,
            map_scale=self.update,
        )


        self.ins_group: InstructionGroup = InstructionGroup()
        self.canvas.add(self.ins_group)


    def adapt_to_map(self, *args):
        super().adapt_to_map(*args)
        self.update()



    def update(self, *args):
        self.ins_group.clear()

        if self.the_map is not None:
            # Prevent negative and div by zero
            scale = min(0.001, self.map_scale)
            # We want to keep square pixels representing
            # square areas, so let's adjust the aspect ratio
            # according to our render area
            w, h = self.size
            
            # This vector goes from the center to the top-right
            # corner
            quarter_viewport = Vector2(w * scale, h * scale)


            self.ins_group.add(MapDrawing(
                self.the_map,
                self.map_center - quarter_viewport,
                self.map_center + quarter_viewport,
                Vector2(*self.pos),
                Vector2(*self.size),
            ))
        

