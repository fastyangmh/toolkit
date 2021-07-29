# import
import cv2
import matplotlib.pyplot as plt
import numpy as np

# def


def get_roi_edges_image(filepath):
    # load image to grayscale
    image = cv2.imread(filepath, 0)

    # get roi
    mask = cv2.inRange(image, 20, 200)  # find black background
    distance = cv2.distanceTransform(mask, cv2.DIST_L2, 5, cv2.CV_32F)
    maxdist = 0
    for i in range(distance.shape[0]):
        for j in range(distance.shape[1]):
            dist = distance[i][j]
            if maxdist < dist:
                x = j
                y = i
                maxdist = dist
    half_slide = maxdist * np.cos(np.pi / 4)
    (left, right, top, bottom) = ((x - half_slide),
                                  (x + half_slide), (y - half_slide), (y + half_slide))
    image = image[int(top):int(bottom), int(left):int(right)]

    # find edges sobel
    sobelX = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(image, cv2.CV_64F, 0, 1)
    sobelX = np.uint8(np.absolute(sobelX))
    sobelY = np.uint8(np.absolute(sobelY))
    edges = cv2.bitwise_or(sobelX, sobelY)

    return edges


if __name__ == '__main__':
    # parameters
    filepath = '/Users/yangmh/Downloads/Original Images/session1/00018.tiff'

    # get roi edges image
    edges = get_roi_edges_image(filepath=filepath)

    # display image
    plt.imshow(edges, cmap='gray')
    plt.show()
