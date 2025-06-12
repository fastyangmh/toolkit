# import
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from toolkit.file_downloader.src.file_downloader import FileDownloader


# class
class TestFileDownloader(unittest.TestCase):
    @patch("toolkit.file_downloader.src.file_downloader.tqdm")
    @patch("toolkit.file_downloader.src.file_downloader.tempfile.mkdtemp")
    @patch("toolkit.file_downloader.src.file_downloader.requests.get")
    def test_download_to_temp_success(self, mock_get, mock_mkdtemp, mock_tqdm):
        url = "http://example.com/file.txt"
        temp_dir = tempfile.gettempdir()

        mock_mkdtemp.return_value = temp_dir
        filename = os.path.basename(url)
        filepath = os.path.join(temp_dir, filename)

        mock_response = Mock()
        mock_response.ok = True
        mock_response.iter_content.return_value = [b"data1", b"data2"]
        mock_get.return_value = mock_response

        mock_tqdm.side_effect = lambda x, **kwargs: x

        result_path = FileDownloader.download_to_temp(url)

        self.assertEqual(result_path, filepath)
        self.assertTrue(os.path.exists(result_path))

        with open(result_path, "rb") as f:
            content = f.read()

        self.assertEqual(content, b"data1data2")

    @patch("toolkit.file_downloader.src.file_downloader.requests.get")
    def test_download_to_temp_failure(self, mock_get):
        url = "http://example.com/file.txt"
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            FileDownloader.download_to_temp(url)


if __name__ == "__main__":
    unittest.main()
