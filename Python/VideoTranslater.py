#import
from torchvision.io import read_video
import torch.nn as nn
import matplotlib.pyplot as plt
from torchvision.transforms.functional import affine


#class
class VideoTranslater(nn.Module):
    def __init__(self, translate_weight: float) -> None:
        super().__init__()
        self.translate_weight = translate_weight

    def forward(self, x, translate_direction: str):
        height, width = x.shape[-2:]
        max_dx = float(self.translate_weight * width)
        max_dy = float(self.translate_weight * height)
        tx, ty = 0, 0
        if translate_direction == 'up':
            ty = -max_dy
        elif translate_direction == 'down':
            ty = max_dy
        elif translate_direction == 'left':
            tx = -max_dx
        elif translate_direction == 'right':
            tx = max_dx
        return affine(img=x,
                      angle=0.,
                      translate=(tx, ty),
                      scale=1.0,
                      shear=(0.0, 0.0))


if __name__ == '__main__':
    #parameters
    filepath = 'video.mp4'
    translate_weight = 0.25
    translate_direction = 'left'

    #load video
    x, _, _ = read_video(filename=filepath,
                         start_pts=0,
                         end_pts=None,
                         pts_unit='sec',
                         output_format='TCHW')
    x = x[:10]

    #create transform
    transform = VideoTranslater(translate_weight=translate_weight)

    #transform
    x = transform(x=x, translate_direction=translate_direction)

    #display
    for v in x:
        plt.imshow(v.permute(1, 2, 0))
        plt.show()