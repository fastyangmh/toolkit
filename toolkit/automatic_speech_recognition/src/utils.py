# import
import importlib
import importlib.util
import inspect
from pathlib import Path


# class
class ClassRegisterHandler:
    def __init__(
        self,
        registry: dict[str, type],
        ignore_filenames: list[str],
    ):
        self._registry = registry
        self.ignore_filename = ignore_filenames

    def register(self, name: str, cls: type):
        if name in self._registry:
            raise ValueError(
                f"Product with name '{name}' already registered. "
                f"Current: {self._registry[name]}, New: {cls}"
            )
        self._registry[name] = cls

    def register_from_dir(self, path: str, base_cls: type):
        for filepath in Path(path).glob(pattern="*.py"):
            if filepath.name in self.ignore_filename:
                continue

            spec = importlib.util.spec_from_file_location(filepath.stem, filepath)

            if spec is None or spec.loader is None:
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    obj.__module__ != filepath.stem
                    or not issubclass(obj, base_cls)
                    or obj is base_cls
                ):
                    continue

                self.register(name, obj)
