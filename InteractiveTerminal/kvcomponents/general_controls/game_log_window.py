from ..shared.centered_label import CenteredLabel
from ...models.app_settings import BOX_WIDTH
from ...models.game import THE_GAME

class GameLogView(CenteredLabel):
    def __init__(self, **kwargs):
        super().__init__(
            text="",
            font_style="Body1",
            box_width=BOX_WIDTH-2,
            box_height=2,
            **kwargs
        )
        THE_GAME.game_log.bind(self.on_log)
    
    def on_log(self, msg):
        self.text = str(msg)
    
