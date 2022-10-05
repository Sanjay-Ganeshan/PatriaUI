from ..shared.centered_label import CenteredLabel
from ...new_models.state.app_settings import BOX_WIDTH
from ...new_models.state.state_manager import StateManager
from ...new_models.events.ev_base import GameOrViewEvent
from ..shared.listens_for_state_changes import ListenForStateChanges

class MiniChatbox(CenteredLabel, ListenForStateChanges):
    def __init__(self, **kwargs):
        super().__init__(
            text="",
            font_style="Body1",
            box_width=BOX_WIDTH-2,
            box_height=2,
            **kwargs
        )
        
        self.listener_init()
    
    def on_log(self, msg):
        self.text = str(msg)

    def listener(self, ev: GameOrViewEvent, is_forward: bool, state_manager: StateManager) -> None:
        if len(state_manager.game_state.chat_log) == 0:
            self.text = "Welcome!"
        else:
            if state_manager.view_state.chat_log_index < 0:
                if state_manager.view_state.chat_log_index >= -1 * len(state_manager.game_state.chat_log):
                    self.text = state_manager.game_state.chat_log[state_manager.view_state.chat_log_index]
                else:
                    self.text = "NO MORE MESSAGES"
            else:
                if state_manager.view_state.chat_log_index < len(state_manager.game_state.chat_log):
                    self.text = state_manager.game_state.chat_log[state_manager.view_state.chat_log_index]
                else:
                    self.text = "NO MORE MESSAGES"
    
