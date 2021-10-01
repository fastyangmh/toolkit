# import
import cv2
import matplotlib.pyplot as plt
import numpy as np

# class


class PalmprintPrincipalLinesExtraction:
    def __init__(self, scaling_coefficient):
        self.scaling_coefficient = scaling_coefficient
        self.kernel0 = np.array([[0., 0., 0., 0., 0.],
                                 [0., 0., 0., 0., 0.],
                                 [0.2, 0.2, 0.2, 0.2, 0.2],
                                 [0., 0., 0., 0., 0.],
                                 [0., 0., 0., 0., 0.]])

        self.kernel45 = np.array([[0.2, 0., 0., 0., 0.],
                                  [0., 0.2, 0., 0., 0.],
                                  [0., 0., 0.2, 0., 0.],
                                  [0., 0., 0., 0.2, 0.],
                                  [0., 0., 0., 0., 0.2]])

        self.kernel90 = np.array([[0., 0., 0.2, 0., 0.],
                                  [0., 0., 0.2, 0., 0.],
                                  [0., 0., 0.2, 0., 0.],
                                  [0., 0., 0.2, 0., 0.],
                                  [0., 0., 0.2, 0., 0.]])

        self.kernel135 = np.array([[0., 0., 0., 0., 0.2],
                                   [0., 0., 0., 0.2, 0.],
                                   [0., 0., 0.2, 0., 0.],
                                   [0., 0.2, 0., 0., 0.],
                                   [0.2, 0., 0., 0., 0.]])

    def __call__(self, image):
        new_image = np.zeros(image.shape, dtype=np.uint8)
        for idx, kernel in enumerate([self.kernel0, self.kernel45, self.kernel90, self.kernel135]):
            # filtering
            if idx == 0:
                img = cv2.filter2D(src=cv2.medianBlur(
                    src=image, ksize=3), ddepth=-1, kernel=kernel)
            else:
                img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)

            # morphology close
            img = cv2.morphologyEx(
                src=img, op=cv2.MORPH_CLOSE, kernel=np.ones((3, 3)))

            # subtract
            img = cv2.subtract(src1=image, src2=img)

            # add
            new_image = cv2.add(src1=new_image, src2=img)

        # reduce noise
        new_image = np.where(new_image <= (
            self.scaling_coefficient * np.mean(new_image)), 0, new_image)

        # binarized
        _, new_image = cv2.threshold(
            new_image, np.mean(new_image), 255, cv2.THRESH_BINARY)

        return new_image


if __name__ == '__main__':
    # parameters
    filepath = 'palm.png'
    scaling_coefficient = 3

    # load image and convert to grayscale
    image = cv2.imread(filename=filepath, flags=0)

    # create object
    obj = PalmprintPrincipalLinesExtraction(
        scaling_coefficient=scaling_coefficient)

    # get palmprint principal lines
    principal_lines = obj(image=image)

    # display image
    plt.subplot(121)
    plt.imshow(image, 'gray')
    plt.subplot(122)
    plt.imshow(principal_lines, 'gray')
    plt.show()
