from kivy.uix.widget import Widget

from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import (
    InstructionGroup,
)

from ...new_models.map.location import Vector2
from ...new_models.map.maps import Map

from ..shared.box_sized_mixin import BoxSized
from ..shared.listens_for_state_changes import ListenForStateChanges
from ...new_models.events.ev_base import GameOrViewEvent
from ...new_models.state.state_manager import StateManager
from .map_instruction import MapDrawing
import typing as T


class MapView(Widget, BoxSized, ListenForStateChanges):
    the_map: Map = ObjectProperty(None)
    map_center: Vector2 = ObjectProperty(Vector2.zero())
    map_scale: float = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=10,
            box_height=10,
            **kwargs,
        )

        self.box_init()
        self.listener_init()

        self.bind(
            pos=self.update,
            size=self.update,
            map_center=self.update,
            map_scale=self.update,
            the_map=self.update,
        )

        self.ins_group: InstructionGroup = InstructionGroup()
        self.canvas.add(self.ins_group)

    def listener(
        self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager
    ) -> None:
        self.the_map = state_manager.game_state.the_map

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

            self.ins_group.add(
                MapDrawing(
                    self.the_map,
                    self.map_center - quarter_viewport,
                    self.map_center + quarter_viewport,
                    Vector2(*self.pos),
                    Vector2(*self.size),
                )
            )
