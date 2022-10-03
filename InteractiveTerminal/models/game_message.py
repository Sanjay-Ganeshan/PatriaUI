# Can be sent to the cloud and replayed

from dataclasses import dataclass, field
from abc import ABC
import uuid

@dataclass
class GameMessage(ABC):
    uid: str = field(default_factory=lambda:str(uuid.uuid1()))

