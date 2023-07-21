#import
from torchvision.io import read_video
import torch.nn as nn
import torch
import matplotlib.pyplot as plt


#class
class VideoRotater(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        #Rotate counterclockwise

    def forward(self, x, k: int):
        #assume x dimension is (T, C, H, W)
        return torch.rot90(input=x, k=k, dims=(-2, -1))


if __name__ == '__main__':
    #parameters
    filepath = 'video.mp4'
    k = 3

    #load video
    x, _, _ = read_video(filename=filepath,
                         start_pts=0,
                         end_pts=None,
                         pts_unit='sec',
                         output_format='TCHW')
    x = x[:10]

    #create transform
    transform = VideoRotater()

    #transform
    x = transform(x, k=k)

    #display
    for v in x:
        plt.imshow(v.permute(1, 2, 0))
        plt.show()