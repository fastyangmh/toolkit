# import
import unittest
from unittest.mock import MagicMock, patch

import cv2

from toolkit.terminal_viewer.src.viewers.video_viewer import VideoViewer


# class
class TestVideoViewer(unittest.TestCase):
    def setUp(self):
        self.viewer = VideoViewer()

    @patch("toolkit.terminal_viewer.src.viewers.video_viewer.cv2.VideoCapture")
    def test_load_data(self, mock_video_capture):
        mock_return = MagicMock(isOpened=MagicMock(return_value=True))
        mock_video_capture.return_value = mock_return

        data = self.viewer._load_data("fake_video.mp4")

        self.assertIsNotNone(data.isOpened())

    @patch(
        "toolkit.terminal_viewer.src.viewers.video_viewer.FileDownloader.download_to_temp"
    )
    @patch("toolkit.terminal_viewer.src.viewers.video_viewer.cv2.VideoCapture")
    def test_load_data_with_http_source(
        self, mock_video_capture, mock_download_to_temp
    ):
        # Simulate download_to_temp returning a local file path
        mock_download_to_temp.return_value = "downloaded_video.mp4"
        mock_video_capture.return_value = MagicMock(
            isOpened=MagicMock(return_value=True)
        )

        data = self.viewer._load_data("http://example.com/video.mp4")

        mock_download_to_temp.assert_called_once_with("http://example.com/video.mp4")
        mock_video_capture.assert_called_once_with("downloaded_video.mp4")
        self.assertIsNotNone(data.isOpened())

    def test_get_metadata(self):
        mock_capture = MagicMock(spec=cv2.VideoCapture)
        mock_capture.get = lambda prop_id: {
            cv2.CAP_PROP_FPS: 10,
            cv2.CAP_PROP_FRAME_COUNT: 5,
            cv2.CAP_PROP_FRAME_WIDTH: 1280,
            cv2.CAP_PROP_FRAME_HEIGHT: 720,
        }.get(prop_id, None)

        metadata = self.viewer._get_metadata(mock_capture)

        self.assertIn("fps", metadata)
        self.assertIn("frame_count", metadata)
        self.assertIn("width", metadata)
        self.assertIn("height", metadata)

    def test_get_metadata_error(self):
        mock_capture = MagicMock(spec=cv2.VideoCapture)
        mock_capture.get = lambda prop_id: {
            cv2.CAP_PROP_FPS: 10,
            cv2.CAP_PROP_FRAME_COUNT: 0,
            cv2.CAP_PROP_FRAME_WIDTH: 1280,
            cv2.CAP_PROP_FRAME_HEIGHT: 720,
        }.get(prop_id, None)

        with self.assertRaises(ValueError):
            self.viewer._get_metadata(mock_capture)

    @patch("toolkit.terminal_viewer.src.viewers.video_viewer.imgcat")
    @patch("toolkit.terminal_viewer.src.viewers.video_viewer.cv2.cvtColor")
    @patch("toolkit.terminal_viewer.src.viewers.video_viewer.tqdm")
    @patch("toolkit.terminal_viewer.src.viewers.video_viewer.time")
    def test_display_data(self, mock_time, mock_tqdm, mock_cvt_color, mock_imgcat):
        mock_capture = MagicMock(spec=cv2.VideoCapture)
        mock_capture.isOpened.side_effect = [True, True, False]
        mock_capture.read.side_effect = [(True, "frame1"), (False, None)]
        mock_capture.set = MagicMock()
        mock_capture.release = MagicMock()

        metadata = {
            "fps": 10,
            "frame_count": 2,
            "width": 1280,
            "height": 720,
        }

        mock_pbar = MagicMock()
        mock_pbar.n = 0
        mock_tqdm.return_value = mock_pbar

        mock_time.perf_counter.side_effect = [0, 0.05, 0.1, 0.15]
        mock_time.sleep = MagicMock()

        mock_cvt_color.return_value = "rgb_frame"

        self.viewer._display_data(
            source="fake_video.mp4",
            data=mock_capture,
            metadata=metadata,
            start_frame=0,
            display_width=80,
            op1="op1_value",
        )

        mock_capture.read.assert_called()
        mock_cvt_color.assert_called_with("frame1", cv2.COLOR_BGR2RGB)
        mock_imgcat.assert_called_with("rgb_frame", width=80, op1="op1_value")
        mock_pbar.update.assert_called_with(1)
        mock_pbar.close.assert_called_once()
        mock_capture.release.assert_called_once()


if __name__ == "__main__":
    unittest.main()
