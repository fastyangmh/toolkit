# import
from torchvision.transforms import RandomErasing
import torch
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# class


class RandomCutMix(RandomErasing):
    def __init__(self, p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3), value=0, inplace=False):
        super().__init__(p=p, scale=scale, ratio=ratio, value=value, inplace=inplace)

    def forward(self, img, source_img):
        if torch.rand(1) < self.p:
            # cast self.value to script acceptable type
            if isinstance(self.value, (int, float)):
                value = [self.value, ]
            elif isinstance(self.value, str):
                value = None
            elif isinstance(self.value, tuple):
                value = list(self.value)
            else:
                value = self.value

            if value is not None and not (len(value) in (1, img.shape[-3])):
                raise ValueError(
                    "If value is a sequence, it should have either a single value or "
                    "{} (number of input channels)".format(img.shape[-3])
                )

            x, y, h, w, _ = self.get_params(
                source_img, scale=self.scale, ratio=self.ratio, value=value)
            img[:, x:w, y:h] = source_img[:, x:w, y:h]
        return img


if __name__ == '__main__':
    # parameters
    img_filepath = 'image.png'
    source_img_filepath = 'source_image.png'
    p = 1

    # create objective
    obj = RandomCutMix(p=p)

    # load image
    img = torch.tensor(
        np.array(Image.open(img_filepath).convert('RGB')).transpose(2, 0, 1))
    source_img = torch.tensor(
        np.array(Image.open(source_img_filepath).convert('RGB')).transpose(2, 0, 1))

    # forward
    new_img = obj(img, source_img)

    # display
    plt.imshow(new_img.numpy().transpose(1, 2, 0))
    plt.show()
