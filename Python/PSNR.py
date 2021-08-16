# import
import torch
from torch.nn.functional import mse_loss
import numpy as np
import cv2
import matplotlib.pyplot as plt

# class


class PSNR:
    def __init__(self):
        pass

    def __call__(self, pred_image, target_image):
        mse = mse_loss(input=pred_image, target=target_image)
        if mse < 1e-10:
            return torch.tensor(100)
        else:
            return 20 * torch.log10(255.0 / mse)


if __name__ == '__main__':
    # parameters
    filepath = 'Screen Recording 2021-08-05 at 11.05.44 AM.mov'
    fps = 60

    # create object
    obj = PSNR()

    # calculate
    psnr_array = []
    video = cv2.VideoCapture(filepath)
    result, previous_image = video.read()
    index = 1
    while result:
        result, image = video.read()
        if result and index == fps:
            psnr_array.append(obj(pred_image=torch.from_numpy(image).float(),
                                  target_image=torch.from_numpy(previous_image).float()).item())
            cv2.imshow('image', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            index = 0
        index += 1
    video.release()
    cv2.destroyAllWindows()

    # plot
    plt.plot(np.linspace(0, int(len(psnr_array)),
                         len(psnr_array)), psnr_array)
    #plt.plot(np.linspace(0, int(len(psnr_array)/fps),len(psnr_array)), np.diff(psnr_array,prepend=0))
    plt.show()
