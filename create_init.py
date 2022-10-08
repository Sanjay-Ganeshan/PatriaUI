import os


def main() -> None:
    project_root = os.path.join(
        os.path.dirname(__file__), "InteractiveTerminal"
    )
    for (root, subdirs, subfns) in os.walk(project_root):
        for fn in subfns:
            if fn == "__init__.py":
                modules = []
                for each_subdir in subdirs:
                    if os.path.isfile(
                        os.path.join(root, each_subdir, "__init__.py")
                    ):
                        modules.append(each_subdir)
                for each_subfn in subfns:
                    if not each_subfn.startswith("__") and each_subfn.endswith(
                        ".py"
                    ):
                        modules.append(each_subfn[:-3])
                with open(os.path.join(root, fn), "w") as f:
                    f.write(f"__all__ = {modules}\n")


if __name__ == "__main__":
    main()
