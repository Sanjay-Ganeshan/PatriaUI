from ..shared.box_sized_mixin import BoxSized
from ..shared.touchable_mixin import TouchableMixin
from kivy.uix.image import Image
from ..resource_list import Resources
from ...models.game import THE_GAME

class CycleViews(Image, BoxSized, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            source=Resources.CYCLE,
            box_width=2,
            box_height=2,
            allow_stretch=True,
            color="blue",
            **kwargs,
        )
        self.box_init()
        self.touch_init()


    def on_left_click(self, position):
        super().on_left_click(position)
        THE_GAME.app.character_sheet.details.switch_view()

