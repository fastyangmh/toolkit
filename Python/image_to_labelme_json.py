#import
import cv2
import base64
import json
from os.path import basename


#def
def get_contour_points(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    points = []
    for ct in contours:
        ct = ct[:, 0]
        points.append([v.tolist() for v in ct])
    return points


def image_to_base64(image):
    s = cv2.imencode(ext='.png', img=image)[1].tobytes()
    return base64.b64encode(s=s)


def image_to_labelme_json(points, labels, filename, image, target_path):
    data = {}
    shapes = []
    for l, p in zip(labels, points):
        shapes.append({'label': l, 'points': p, 'shape_type': 'polygon'})
    data['shapes'] = shapes
    data['imagePath'] = filename
    data['imageData'] = image_to_base64(image=image).decode(encoding='utf-8')
    height, width = image.shape
    data['imageHeight'] = height
    data['imageWidth'] = width

    with open(target_path, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    #parameters
    filename = 'image.png'

    #load image
    image = cv2.imread(filename=filename,
                       flags=0)  #the mask image needs be a graylscale image

    #get contour points
    points = get_contour_points(image=image)

    #save to json file
    image_to_labelme_json(points=points,
                          labels=['forgeground'] * len(points),
                          filename=filename,
                          image=image,
                          target_path=basename(filename)[:-3] + 'json')
