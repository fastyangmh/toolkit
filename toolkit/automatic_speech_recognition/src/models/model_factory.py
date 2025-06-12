# import
from pathlib import Path

from toolkit.automatic_speech_recognition.src.constants import MODELS_DIRECTORY
from toolkit.automatic_speech_recognition.src.models import BaseASRModel
from toolkit.automatic_speech_recognition.src.utils import ClassRegisterHandler


# class
class ModelFactory:
    registry = {}
    if not registry:
        class_register_handler = ClassRegisterHandler(
            registry,
            ["__init__.py", Path(__file__).name],
        )
        class_register_handler.register_from_dir(
            path=MODELS_DIRECTORY, base_cls=BaseASRModel
        )

    @classmethod
    def build(cls, model_type: str, model_info: dict) -> BaseASRModel:
        if model_type not in cls.registry:
            raise KeyError(
                f"Model type '{model_type}' not found in registry. "
                f"Available types: {tuple(cls.registry.keys())}"
            )

        model_cls = cls.registry[model_type]
        model = model_cls(**model_info)

        return model
