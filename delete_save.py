from InteractiveTerminal.save.file_io import path_for
from pathlib import Path

if __name__ == "__main__":
    p = Path(path_for("STATE"))
    if p.is_file():
        p.unlink()