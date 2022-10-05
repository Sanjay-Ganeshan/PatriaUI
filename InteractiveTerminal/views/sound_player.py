from kivy.core.audio import SoundLoader, Sound
from .resource_list import Resources
import typing as T

class SoundPlayer:
    dice_rolls: T.List[Sound] = [SoundLoader.load(sf) for sf in Resources.SFX_DICE_ROLL]
    keypress: Sound = SoundLoader.load(Resources.SFX_KEYPRESS)
