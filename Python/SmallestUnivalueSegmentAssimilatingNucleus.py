'''
follow as https://github.com/rajatjain3571/Susan-Corner-Detection to implement
'''

# import
import numpy as np
import cv2
import matplotlib.pyplot as plt

# class


class SmallestUnivalueSegmentAssimilatingNucleus:
    def __init__(self):
        self.mask = self.susan_mask()

    def susan_mask(self):
        mask = np.ones((7, 7))
        rows = [0, 0, 0, 0, 1, 1, 5, 5, 6, 6, 6, 6]
        cols = [0, 1, 5, 6, 0, 6, 0, 6, 0, 1, 5, 6]
        for r, c in zip(rows, cols):
            mask[r, c] = 0
        return mask

    def __call__(self, image):
        image = image.astype(np.float64)
        g = 37/2
        output = np.zeros(image.shape)
        for i in range(3, image.shape[0]-3):
            for j in range(3, image.shape[1]-3):
                ir = np.array(image[i-3:i+4, j-3:j+4])
                ir = ir[self.mask == 1]
                ir0 = image[i, j]
                a = np.sum(np.exp(-((ir-ir0)/10)**6))
                if a <= g:
                    a = g-a
                else:
                    a = 0
                output[i, j] = a
        return output


if __name__ == '__main__':
    # parameters
    filepath = 'susan_input1.png'

    # load image and convert to grayscale
    image = cv2.imread(filename=filepath, flags=0)

    # create SUSAN object
    susan = SmallestUnivalueSegmentAssimilatingNucleus()

    # get corner
    corner = susan(image=image)

    # display
    plt.subplot(121)
    plt.imshow(image, 'gray')
    plt.subplot(122)
    plt.imshow(corner, 'gray')
    plt.show()
