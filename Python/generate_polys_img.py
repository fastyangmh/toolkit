#import
import cv2
import numpy as np
import matplotlib.pyplot as plt


#def
def generate_polys_img(height, width, pts):
    img = np.zeros(shape=(height, width), dtype=np.uint8)
    for idx, v in enumerate(pts):
        img = cv2.fillPoly(img=img, pts=[np.array(v)], color=1 + idx)
    return img


if __name__ == '__main__':
    #parameters
    height = 1080
    width = 1920
    pts = [[(1230, 1075), (1428, 606), (1609, 652), (1589, 1073)],
           [(120, 657), (235, 400), (567, 479)],
           [(233, 173), (875, 425), (528, 192), (862, 132), (328, 873)]]

    #generate
    polys_img = generate_polys_img(height=height, width=width, pts=pts)

    #display
    plt.imshow(polys_img)
    plt.show()