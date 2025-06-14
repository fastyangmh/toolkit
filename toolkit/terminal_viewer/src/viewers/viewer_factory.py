# import
from pathlib import Path

from toolkit.class_register_handler import ClassRegisterHandler
from toolkit.terminal_viewer.src.constants import VIEWERS_DIRECTORY
from toolkit.terminal_viewer.src.viewers import BaseViewer


# class
class ViewerFactory:
    registry = {}
    if not registry:
        class_register_handler = ClassRegisterHandler(
            registry,
            ["__init__.py", Path(__file__).name],
        )
        class_register_handler.register_from_dir(
            path=VIEWERS_DIRECTORY, base_cls=BaseViewer
        )

    @classmethod
    def build(cls, viewer_type: str, viewer_info: dict) -> BaseViewer:
        if viewer_type not in cls.registry:
            raise KeyError(
                f"Viewer type '{viewer_type}' not found in registry. "
                f"Available types: {tuple(cls.registry.keys())}"
            )

        viewer_cls = cls.registry[viewer_type]

        return viewer_cls(**viewer_info)
