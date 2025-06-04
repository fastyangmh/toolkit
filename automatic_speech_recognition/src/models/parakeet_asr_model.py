# import
from typing import Sequence

import mlx.core as mx
from parakeet_mlx import from_pretrained
from parakeet_mlx.parakeet import BaseParakeet

from src.models.base_asr_model import BaseASRModel


# class
class ParakeetASRModel(BaseASRModel):
    def __init__(self, model_id: str, use_fp32: bool) -> None:
        super().__init__()

        float_precision_type: mx.Dtype = mx.bfloat16 if not use_fp32 else mx.float32
        model = self._load_model(
            model_id,
            float_precision_type,
        )

        self.model = model
        self.float_precision_type = float_precision_type

    def _load_model(
        self, model_id: str, float_precision_type: mx.Dtype
    ) -> BaseParakeet:
        return from_pretrained(
            model_id,
            dtype=float_precision_type,
        )

    def transcribe(self, inputs: Sequence[str], *args, **kwargs) -> list[str]:
        outputs = []

        for path in inputs:
            if not isinstance(path, str):
                raise ValueError(f"Expected string path, got {type(path)}")

            result = self.model.transcribe(
                path,
                dtype=self.float_precision_type,
                chunk_duration=kwargs.get("chunk_duration", 120),
                overlap_duration=kwargs.get("overlap_duration", 15),
            )

            output = "".join([sentence.text for sentence in result.sentences])
            outputs.append(output)

        return outputs
