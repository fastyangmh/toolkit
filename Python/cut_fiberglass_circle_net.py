# import
import cv2
import numpy as np
import matplotlib.pyplot as plt

# def


def get_roi_image(filepath):

    # load image
    image = cv2.imread(filename=filepath, flags=cv2.IMREAD_GRAYSCALE)

    # denoise
    blurred = cv2.medianBlur(src=image, ksize=7)

    # find edge
    edge = cv2.Canny(image=blurred, threshold1=30, threshold2=150)
    edge = cv2.dilate(src=edge, kernel=np.ones(
        shape=(3, 3), dtype=np.uint8), iterations=20)

    # find maximum contour
    contours, _ = cv2.findContours(
        image=edge, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(contours)

    # get roi image
    #mask = edge[y:y+h, x:x+w]
    #image = image[y:y+h, x:x+w]
    #image = cv2.bitwise_and(src1=image, src2=mask)
    return image[y:y+h, x:x+w]


if __name__ == '__main__':
    # parameters
    filepath = 'good_00001.png'

    # get roi image
    image = get_roi_image(filepath=filepath)

    # display image
    plt.imshow(image, cmap='gray')
    plt.show()
