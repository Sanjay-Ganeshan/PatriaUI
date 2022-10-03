from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants
from kivy.uix.image import Image
from ..shared.touchable_mixin import TouchableMixin

class CHIcon(Image, BoxSized, NeedsConstants, TouchableMixin):
    def __init__(self, **kwargs):
        super().__init__(
            source="",
            box_width=1,
            box_height=3,
            allow_stretch=True,
            **kwargs,
        )
        self.box_init()
        self.constants_init()
        self.touch_init()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.source = self.constants.ICON_SRC

    def on_left_click(self, position):
        from ...models.game import THE_GAME
        THE_GAME.change_character()
