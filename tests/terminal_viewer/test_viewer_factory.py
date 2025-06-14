# import
import unittest

from toolkit.terminal_viewer.src.viewers import BaseViewer, ViewerFactory


# class
class DummyViewer(BaseViewer):
    def __init__(self, value1: int, value2: int):
        self.value1 = value1
        self.value2 = value2

    def _load_data(self, source: str):
        pass

    def _get_metadata(self, data: str):
        pass

    def _display_data(self, data: str, metadata: dict[str, int] | None):
        pass


class TestViewerFactory(unittest.TestCase):
    def setUp(self) -> None:
        ViewerFactory.registry = {"dummy": DummyViewer}

    def test_build_success(self):
        viewer_info = {"value1": 1, "value2": 2}

        viewer = ViewerFactory.build("dummy", viewer_info)

        self.assertIsInstance(viewer, DummyViewer)
        self.assertEqual(getattr(viewer, "value1"), 1)
        self.assertEqual(getattr(viewer, "value2"), 2)


if __name__ == "__main__":
    unittest.main()
