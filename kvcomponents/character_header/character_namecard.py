from ..shared.centered_label import CenteredLabel
from ..shared.box_sized_mixin import BoxSized
from ..shared.needs_character_mixin import NeedsConstants


class CHNamecard(CenteredLabel, BoxSized, NeedsConstants):
    def __init__(self, **kwargs):
        super().__init__(
            text="",
            box_width=1.5,
            box_height=3,
            font_style="H5",
            **kwargs,
        )
        self.box_init()
        self.constants_init()

    def adapt_to_constants(self, *args):
        super().adapt_to_constants(*args)
        self.text = f"{self.constants.CHARACTER_NAME}\n{self.constants.CHARACTER_ROLE}"
