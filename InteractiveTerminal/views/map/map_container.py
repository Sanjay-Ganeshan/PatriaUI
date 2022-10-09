from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import ObjectProperty, NumericProperty

from ...new_models.map.location import Vector2

from ..shared.box_sized_mixin import BoxSized
from ..shared.spacer import Spacer
from ..shared.listens_for_state_changes import ListenForStateChanges
from ...new_models.state.app_settings import BOX_WIDTH
from .map_view import MapView
import typing as T


class MapContainer(MDBoxLayout, BoxSized, ListenForStateChanges):
    map_center: ObjectProperty = ObjectProperty(Vector2.zero())
    map_scale: NumericProperty = NumericProperty(1.0)
    the_map: ObjectProperty = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(
            box_width=BOX_WIDTH,
            box_height=10,
            orientation="horizontal",
            **kwargs
        )

        self.toolbox = Spacer(box_width=2, box_height=10)
        self.view = MapView()

        self.box_init()
        self.listener_init()

        self.add_widget(self.toolbox)
        self.add_widget(self.view)

        self.bind(map_center=self.update_view, map_scale=self.update_view)

        self.update_view()

    def update_view(self, *args):
        self.view.map_center = self.map_center
        self.view.map_scale = self.map_scale
