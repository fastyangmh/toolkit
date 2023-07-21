#import
import cv2
import numpy as np
import matplotlib.pyplot as plt


#def
def polys_iou(polys_img, xyxy):
    obj_img = cv2.rectangle(img=np.zeros_like(a=polys_img, dtype=np.uint8),
                            pt1=xyxy[:2],
                            pt2=xyxy[2:],
                            color=1,
                            thickness=-1)
    obj_area = abs((xyxy[0] - xyxy[2]) * (xyxy[1] - xyxy[3]))
    intersection = obj_img * polys_img

    result = []
    if np.sum(intersection):
        roi_ids = np.unique(intersection)
        for roi_id in roi_ids:
            if roi_id == 0:
                continue
            inter = np.sum(intersection == roi_id)
            union = np.sum(polys_img == roi_id) + obj_area - inter
            result.append([inter / union, roi_id])
    return result


if __name__ == '__main__':
    #parameters
    height = 1080
    width = 1920
    boxes = [[972, 713, 1343, 1049], [454, 413, 665, 1055],
             [303, 296, 1484, 1009]]

    poly_pts = [[(1429, 608), (1234, 1080), (1500, 1080), (1616, 649)],
                [(899, 206), (866, 850), (1127, 924), (1226, 825), (1295, 205),
                 (1053, 165)],
                [(14, 236), (74, 828), (303, 975), (504, 846), (460, 206),
                 (222, 175)]]

    #initial polys_img
    polys_img = np.zeros(shape=(height, width), dtype=np.uint8)
    for idx, v in enumerate(poly_pts):
        polys_img = cv2.fillPoly(img=polys_img,
                                 pts=np.array(v)[None],
                                 color=1 + idx)

    #display
    plt.imshow(polys_img)
    plt.show()

    #calculate iou
    for v in boxes:
        print(polys_iou(polys_img=polys_img, xyxy=v))
