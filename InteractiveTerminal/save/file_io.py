import os
import json
import typing as T

MYDIR = os.path.dirname(os.path.abspath(__file__))

def path_for(name: str) -> None:
    return os.path.join(MYDIR, f"{name}.json")

def save(obj, name: str) -> None:
    with open(os.path.join(MYDIR, f"{name}.json"), "w") as f:
        json.dump(obj, f, indent=4)

def load(name: str) -> T.Any:
    with open(os.path.join(MYDIR, f"{name}.json"), "r") as f:
        return json.load(f)
    
def query() -> T.List[str]:
    return [b for (b,e) in (
        os.path.splitext(fn) for fn in sorted(os.listdir(MYDIR))
    ) if e == ".json"]