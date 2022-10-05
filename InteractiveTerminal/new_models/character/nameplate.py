from dataclasses import dataclass


@dataclass
class Nameplate:
    """
    Name information about a character
    """
    icon: str = "missing.png"
    name: str = "<name>"
    role: str = "<role>"
    
    she: str = "<she>"
    her: str = "<her>"
    hers: str = "<hers>"
