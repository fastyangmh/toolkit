# import
import unittest
from typing import Any
from unittest.mock import MagicMock

from toolkit.terminal_viewer.src.viewers import BaseViewer


# class
class ConcreteViewer(BaseViewer):
    def _load_data(self, source: Any) -> Any: ...
    def _get_metadata(self, data: Any) -> dict[str, Any]: ...
    def _display_data(
        self,
        source: Any,
        data: Any,
        metadata: dict[str, Any],
        **kwargs,
    ) -> None: ...


class TestBaseViewer(unittest.TestCase):
    def test_display_calls_methods(self):
        viewer = ConcreteViewer()
        viewer._load_data = MagicMock()
        viewer._get_metadata = MagicMock()
        viewer._display_data = MagicMock()
        source = "test_source"
        viewer.display(source)

        viewer._load_data.assert_called_once_with(source)
        viewer._get_metadata.assert_called_once_with(viewer._load_data.return_value)
        viewer._display_data.assert_called_once_with(
            source,
            viewer._load_data.return_value,
            viewer._get_metadata.return_value,
        )


if __name__ == "__main__":
    unittest.main()
