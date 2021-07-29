# import
import cv2
import matplotlib.pyplot as plt
import numpy as np

# def


def load_image(filepath):
    return cv2.imread(filepath)


def mask_image_by_hsv(image, lower, upper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    masked_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    return masked_image


def get_roi(masked_image_by_hsv):
    mask_binary = cv2.inRange(masked_image_by_hsv, 10,
                              240)  # find black background
    distance = cv2.distanceTransform(mask_binary, cv2.DIST_L1, 3, cv2.CV_32F)
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
    roi = masked_image_by_hsv[int(top):int(bottom), int(left):int(right)]
    return roi


def get_edges(roi_image):
    sobelX = cv2.Sobel(roi_image, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(roi_image, cv2.CV_64F, 0, 1)
    sobelX = np.uint8(np.absolute(sobelX))
    sobelY = np.uint8(np.absolute(sobelY))
    edges = cv2.bitwise_or(sobelX, sobelY)
    return edges


if __name__ == '__main__':
    # parameters
    filepath = '/Users/yangmh/Desktop/image.jpeg'
    lower = np.array([0, 50, 50])
    upper = np.array([20, 255, 255])

    # load image to grayscale
    image = load_image(filepath=filepath)

    # get masked image by hsv
    masked_image_by_hsv = mask_image_by_hsv(
        image=image, lower=lower, upper=upper)

    # get roi image
    roi_image = get_roi(masked_image_by_hsv=masked_image_by_hsv)

    # get edges
    edges = get_edges(roi_image=roi_image)

    # display image
    plt.subplot(141)
    plt.title('orginal image')
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.subplot(142)
    plt.title('masked image by hsv')
    plt.imshow(masked_image_by_hsv, cmap='gray')
    plt.subplot(143)
    plt.title('region of interest')
    plt.imshow(roi_image, cmap='gray')
    plt.subplot(144)
    plt.title('edges')
    plt.imshow(edges, cmap='gray')
    plt.show()
