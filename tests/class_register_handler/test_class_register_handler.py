# import
import os
import sys
import tempfile
import unittest

from toolkit.class_register_handler.src import ClassRegisterHandler


# class
class DummyBase:
    pass


class DummyChild(DummyBase):
    pass


class TestClassRegisterHandler(unittest.TestCase):
    def setUp(self):
        self.registry = {}
        self.ignore_filenames = ["ignore.py"]
        self.handler = ClassRegisterHandler(self.registry, self.ignore_filenames)

    def test_register_success(self):
        self.handler.register("DummyChild", DummyChild)
        self.assertIn("DummyChild", self.registry)
        self.assertIs(self.registry["DummyChild"], DummyChild)

    def test_register_duplicate_raises(self):
        self.handler.register("DummyChild", DummyChild)
        with self.assertRaises(ValueError):
            self.handler.register("DummyChild", DummyChild)

    def test_register_from_dir_registers_classes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "mod1.py")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(
                    (
                        "from tests.class_register_handler.test_class_register_handler import DummyBase\n"
                        "class DummyChild(DummyBase):\n    pass\n"
                        "class DummyOther:\n    pass"
                    )
                )

            ignore_path = os.path.join(tmpdir, "ignore.py")
            with open(ignore_path, "w", encoding="utf-8") as f:
                f.write(
                    (
                        "from tests.class_register_handler.test_class_register_handler import DummyBase\n"
                        "class DummyChildIgnore(DummyBase):\n    pass\n"
                        "class DummyOtherIgnore:\n    pass"
                    )
                )

            sys.path.insert(0, tmpdir)
            try:
                registry = {}
                handler = ClassRegisterHandler(registry, ignore_filenames=["ignore.py"])
                handler.register_from_dir(tmpdir, DummyBase)

                self.assertEqual(len(registry), 1)
                self.assertIn("DummyChild", handler._registry)
                self.assertNotIn("DummyBase", handler._registry)
            finally:
                sys.path.pop(0)


if __name__ == "__main__":
    unittest.main()
