#import
import torch
import pytorchvideo
from pytorchvideo.data.encoded_video import EncodedVideo
from torchvision.transforms import Compose, Lambda
from torchvision.transforms._transforms_video import (
    CenterCropVideo,
    NormalizeVideo,
)
from pytorchvideo.transforms import (ApplyTransformToKey, ShortSideScale,
                                     UniformTemporalSubsample)
import cv2
import numpy as np
import torch.nn as nn


#class
class VideoFeatureExtractor:
    def __init__(self, model_name, device) -> None:
        #create model
        model = torch.hub.load('facebookresearch/pytorchvideo',
                               model_name,
                               pretrained=True)
        model.blocks[5].proj = nn.Identity()
        model.blocks[5].activation = nn.Identity()
        model.blocks[5].output_pool = nn.Identity()
        model = model.eval()
        model = model.to(device)
        self.model = model

        #define transform
        mean = [0.45, 0.45, 0.45]
        std = [0.225, 0.225, 0.225]
        model_transform_params = {
            "x3d_xs": {
                "side_size": 182,
                "crop_size": 182,
                "num_frames": 4,
                "sampling_rate": 12,
            },
            "x3d_s": {
                "side_size": 182,
                "crop_size": 182,
                "num_frames": 13,
                "sampling_rate": 6,
            },
            "x3d_m": {
                "side_size": 256,
                "crop_size": 256,
                "num_frames": 16,
                "sampling_rate": 5,
            }
        }
        transform_params = model_transform_params[model_name]
        self.transform = ApplyTransformToKey(
            key="video",
            transform=Compose([
                UniformTemporalSubsample(transform_params["num_frames"]),
                Lambda(lambda x: x / 255.0),
                NormalizeVideo(mean, std),
                ShortSideScale(size=transform_params["side_size"]),
                CenterCropVideo(crop_size=(transform_params["crop_size"],
                                           transform_params["crop_size"]))
            ]),
        )
        self.transform_params = transform_params
        self.device = device

    def video2inputs(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_counts = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = int(np.ceil(frame_counts / fps))
        inputs = []
        clip_duration = (
            self.transform_params["num_frames"] *
            self.transform_params["sampling_rate"]) / fps  #frames_per_second
        for start_sec in range(duration):
            video = EncodedVideo.from_path(video_path)
            end_sec = start_sec + clip_duration
            video_data = video.get_clip(start_sec=start_sec, end_sec=end_sec)
            if video_data['video'] is not None:
                video_data = self.transform(video_data)
                inputs.append(video_data["video"])
            else:
                break
        inputs = torch.stack(inputs, 0)
        inputs = inputs.to(self.device)
        return inputs

    def __call__(self, video_path, mean):
        inputs = self.video2inputs(video_path=video_path)
        with torch.no_grad():
            features = self.model(inputs)
        if mean:
            features = features.mean(0)
        return features


if __name__ == '__main__':
    #parameters
    model_name = 'x3d_m'
    device = "cpu"
    video_path = 'utint_1_1_kick.mp4'
    mean = True

    #create extractor
    extractor = VideoFeatureExtractor(model_name=model_name, device=device)

    #get features
    features = extractor(video_path=video_path, mean=mean)