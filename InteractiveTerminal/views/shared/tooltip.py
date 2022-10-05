from kivymd.uix.tooltip import MDTooltip
from ...new_models.state.app_settings import AppSettings

import typing as T


class OptionalTooltip(MDTooltip):
    def display_tooltip(self, interval: T.Union[int, float]) -> None:
        if AppSettings.TooltipsEnabled:
            super().display_tooltip(interval)
