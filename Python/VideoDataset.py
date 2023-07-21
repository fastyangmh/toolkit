#import
from torchvision.datasets.vision import VisionDataset
from torchvision.datasets.folder import find_classes, make_dataset
from typing import Optional, Callable, Tuple, Dict, Any
from torchvision.datasets.video_utils import VideoClips
from torch import Tensor


#class
class VideoDataset(VisionDataset):
    def __init__(self,
                 root: str,
                 extensions: Tuple,
                 frames_per_clip: int,
                 step_between_clips: int = 1,
                 frame_rate: Optional[int] = None,
                 _precomputed_metadata: Optional[Dict[str, Any]] = None,
                 num_workers: int = 1,
                 _video_width: int = 0,
                 _video_height: int = 0,
                 _video_min_dimension: int = 0,
                 _audio_samples: int = 0,
                 output_format: str = "THWC",
                 transform: Optional[Callable] = None,
                 target_transform: Optional[Callable] = None) -> None:
        super().__init__(root)
        self.classes, class_to_idx = find_classes(self.root)
        self.samples = make_dataset(self.root,
                                    class_to_idx,
                                    extensions,
                                    is_valid_file=None)
        video_list = [x[0] for x in self.samples]
        video_clips = VideoClips(
            video_list,
            frames_per_clip,
            step_between_clips,
            frame_rate,
            _precomputed_metadata,
            num_workers=num_workers,
            _video_width=_video_width,
            _video_height=_video_height,
            _video_min_dimension=_video_min_dimension,
            _audio_samples=_audio_samples,
            output_format=output_format,
        )
        self.full_video_clips = video_clips
        self.video_clips = video_clips
        self.transform = transform
        self.target_transform = target_transform

    @property
    def metadata(self) -> Dict[str, Any]:
        return self.full_video_clips.metadata

    def __len__(self) -> int:
        return self.video_clips.num_clips()

    def __getitem__(self, idx: int) -> Tuple[Tensor, Tensor, int]:
        video, audio, info, video_idx = self.video_clips.get_clip(idx)
        label = self.samples[video_idx][1]

        if self.transform is not None:
            video = self.transform(video)

        if self.target_transform is not None:
            label = self.target_transform(label)

        return video, label


if __name__ == '__main__':
    #parameters
    root = 'UCF-101'
    extensions = ('.avi')
    frames_per_clip = 48
    step_between_clips = 48
    frame_rate = 15
    num_workers = 12
    output_format = 'TCHW'
    transform = None
    target_transform = None
    #
    dataset = VideoDataset(root=root,
                           extensions=extensions,
                           frames_per_clip=frames_per_clip,
                           step_between_clips=step_between_clips,
                           frame_rate=frame_rate,
                           num_workers=num_workers,
                           output_format=output_format,
                           transform=transform,
                           target_transform=target_transform)
