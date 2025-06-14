# import
import unittest
from unittest.mock import MagicMock, patch

from PIL import Image

from toolkit.terminal_viewer.src.viewers.image_viewer import ImageViewer


# class
class TestImageViewer(unittest.TestCase):
    def setUp(self):
        self.viewer = ImageViewer()

    @patch("toolkit.terminal_viewer.src.viewers.image_viewer.Image.open")
    def test_load_data(self, mock_open):
        mock_img = MagicMock(spec=Image.Image)
        mock_open.return_value = mock_img

        result = self.viewer._load_data("fake_path.png")

        mock_open.assert_called_once_with("fake_path.png")
        self.assertEqual(result, mock_img)

    @patch(
        "toolkit.terminal_viewer.src.viewers.image_viewer.FileDownloader.download_to_temp"
    )
    @patch("toolkit.terminal_viewer.src.viewers.image_viewer.Image.open")
    def test_load_data_with_url(self, mock_open, mock_download):
        mock_img = MagicMock(spec=Image.Image)
        mock_open.return_value = mock_img
        mock_download.return_value = "temp_file.png"

        result = self.viewer._load_data("https://example.com/image.png")

        mock_download.assert_called_once_with("https://example.com/image.png")
        mock_open.assert_called_once_with("temp_file.png")
        self.assertEqual(result, mock_img)

    def test_get_metadata(self):
        mock_img = MagicMock(spec=Image.Image)
        mock_img.size = (100, 200)

        metadata = self.viewer._get_metadata(mock_img)

        self.assertEqual(metadata, {"width": 100, "height": 200})

    @patch("toolkit.terminal_viewer.src.viewers.image_viewer.imgcat")
    def test_display_data(self, mock_imgcat):
        mock_img = MagicMock(spec=Image.Image)
        metadata = {"width": 50, "height": 60}

        with patch("builtins.print") as mock_print:
            self.viewer._display_data(
                "img.png", mock_img, metadata, display_width=123, opt1="val1"
            )

            mock_print.assert_any_call("Displaying image from: img.png")
            mock_print.assert_any_call("Image size: 50x60")
            mock_imgcat.assert_called_once_with(mock_img, width=123, opt1="val1")


if __name__ == "__main__":
    unittest.main()
