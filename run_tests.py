import sys
sys.dont_write_bytecode = True

import importlib
import unittest
import typing as T

def get_recursive_modules(module_name: str) -> T.Generator[str, None, None]:
    yield module_name
    mod = importlib.import_module(module_name)
    
    if hasattr(mod, "__all__"):
        for each_submodule in mod.__all__:
            yield from get_recursive_modules(f"{module_name}.{each_submodule}")

def populate_test_cases(modules: T.List[str]) -> T.Generator[T.Tuple[str, unittest.TestCase], None, None]:
    for module_name in modules:
        base_name = module_name.split(".")[-1]        
        if not base_name.startswith("test_"):
            continue
        mod = importlib.import_module(module_name)
        attr_names = dir(mod)
        for each_attr in attr_names:
            attr_val = getattr(mod, each_attr)
            if isinstance(attr_val, type) and issubclass(attr_val, unittest.TestCase):
                yield f"{module_name}.{each_attr}", attr_val

def run_tests(tests: T.List[T.Tuple[str, unittest.TestCase]]) -> bool:
    suite = unittest.TestSuite()
    for (_name, each_test) in tests:
        test_names = [prop for prop in dir(each_test) if prop.startswith("test_")]
        for each_test_name in test_names:
            suite.addTest(each_test(each_test_name))
    runner = unittest.TextTestRunner()
    runner.run(suite)


def main() -> None:
    module_to_test = "InteractiveTerminal"

    all_modules = sorted(get_recursive_modules(module_to_test))
    run_tests(list(populate_test_cases(all_modules)))
    
    

if __name__ == "__main__":
    main()