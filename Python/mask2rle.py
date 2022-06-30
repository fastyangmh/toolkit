#import
from matplotlib import pyplot as plt
import numpy as np


#def
def mask2rle(img):
    img = img.T
    pixels = img.flatten()
    pixels = np.concatenate([[0], pixels, [0]])
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2]
    return ' '.join(str(x) for x in runs)


if __name__ == '__main__':
    #parameters
    weight = 20
    height = 20

    #generate fake mask
    mask = np.random.randint(low=0, high=2, size=(weight, height))

    #convert mask to rle
    rle = mask2rle(img=mask)

    #display
    print(rle)
    plt.imshow(mask)
    plt.show()