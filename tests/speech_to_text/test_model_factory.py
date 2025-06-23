# import
import unittest
from typing import Any, Sequence

from toolkit.speech_to_text.src import BaseModel, ModelFactory


# class
class DummyModel(BaseModel):
    def __init__(self, value1: int, value2: int):
        self.value1 = value1
        self.value2 = value2

    def transcribe(self, inputs: Sequence[Any], *args, **kwargs) -> Any:
        pass


class TestModelFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ModelFactory.registry = {"dummy": DummyModel}

    def test_build_returns_instance(self):
        model_info = {"value1": 1, "value2": 2}

        result = ModelFactory.build("dummy", model_info)

        self.assertIsInstance(result, DummyModel)
        self.assertEqual(result.value1, 1)  # type: ignore
        self.assertEqual(result.value2, 2)  # type: ignore

    def test_build_invalid_type_raises(self):
        with self.assertRaises(KeyError):
            ModelFactory.build("nonexistent", {})

    def test_registry_contains_dummy(self):
        self.assertIn("dummy", ModelFactory.registry)
        self.assertIs(ModelFactory.registry["dummy"], DummyModel)


if __name__ == "__main__":
    unittest.main()
