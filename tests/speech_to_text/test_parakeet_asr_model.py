# import
import unittest
from unittest.mock import MagicMock, patch

import mlx.core as mx
from parakeet_mlx.parakeet import BaseParakeet

from toolkit.speech_to_text.src.models.parakeet_model import ParakeetModel


# class
class TestParakeetModel(unittest.TestCase):
    @patch("toolkit.speech_to_text.src.models.parakeet_model.from_pretrained")
    def test_init_fp32(self, mock_from_pretrained):
        mock_model = MagicMock(spec=BaseParakeet)
        mock_from_pretrained.return_value = mock_model

        model = ParakeetModel("test-model", use_fp32=True)
        self.assertEqual(model.model, mock_model)
        self.assertEqual(model.float_precision_type, mx.float32)

    @patch("toolkit.speech_to_text.src.models.parakeet_model.from_pretrained")
    def test_init_bfloat16(self, mock_from_pretrained):
        mock_model = MagicMock(spec=BaseParakeet)
        mock_from_pretrained.return_value = mock_model

        model = ParakeetModel("test-model", use_fp32=False)
        self.assertEqual(model.model, mock_model)
        self.assertEqual(model.float_precision_type, mx.bfloat16)

    @patch("toolkit.speech_to_text.src.models.parakeet_model.from_pretrained")
    def test_load_model(self, mock_from_pretrained):
        mock_model = MagicMock(spec=BaseParakeet)
        mock_from_pretrained.return_value = mock_model

        model = ParakeetModel._load_model(
            MagicMock(),
            "test-model",
            mx.float32,
        )
        self.assertEqual(model, mock_model)
        mock_from_pretrained.assert_called_once_with("test-model", dtype=mx.float32)

    @patch("toolkit.speech_to_text.src.models.parakeet_model.from_pretrained")
    def test_load_model_called_with_correct_args(self, mock_from_pretrained):
        mock_model = MagicMock()
        mock_from_pretrained.return_value = mock_model

        model = ParakeetModel("some-id", use_fp32=True)
        mock_from_pretrained.assert_called_with(
            "some-id", dtype=model.float_precision_type
        )

    @patch("toolkit.speech_to_text.src.models.parakeet_model.from_pretrained")
    def test_transcribe_success(self, mock_from_pretrained):
        mock_sentence = MagicMock()
        mock_sentence.text = "hello "
        mock_result = MagicMock()
        mock_result.sentences = [mock_sentence, mock_sentence]
        mock_model = MagicMock()
        mock_model.transcribe.return_value = mock_result
        mock_from_pretrained.return_value = mock_model

        model = ParakeetModel("test-model", use_fp32=True)
        result = model.transcribe(["audio1.wav"])
        self.assertEqual(result, ["hello hello "])
        mock_model.transcribe.assert_called_once_with(
            "audio1.wav",
            dtype=model.float_precision_type,
            chunk_duration=120,
            overlap_duration=15,
        )

    @patch("toolkit.speech_to_text.src.models.parakeet_model.from_pretrained")
    def test_transcribe_with_custom_kwargs(self, mock_from_pretrained):
        mock_sentence = MagicMock()
        mock_sentence.text = "foo"
        mock_result = MagicMock()
        mock_result.sentences = [mock_sentence]
        mock_model = MagicMock()
        mock_model.transcribe.return_value = mock_result
        mock_from_pretrained.return_value = mock_model

        model = ParakeetModel("test-model", use_fp32=True)
        result = model.transcribe(["audio2.wav"], chunk_duration=10, overlap_duration=2)
        self.assertEqual(result, ["foo"])
        mock_model.transcribe.assert_called_once_with(
            "audio2.wav",
            dtype=model.float_precision_type,
            chunk_duration=10,
            overlap_duration=2,
        )

    @patch("toolkit.speech_to_text.src.models.parakeet_model.from_pretrained")
    def test_transcribe_invalid_input_type(self, mock_from_pretrained):
        mock_model = MagicMock()
        mock_from_pretrained.return_value = mock_model
        model = ParakeetModel("test-model", use_fp32=True)
        with self.assertRaises(ValueError):
            model.transcribe([123])  # type: ignore


if __name__ == "__main__":
    unittest.main()
