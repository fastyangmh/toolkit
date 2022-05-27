#import
import cv2
from time import time

if __name__ == '__main__':
    #parameters
    username = 'xxxxxxxxxx'
    password = 'xxxxxxxxxx'
    ip = 'xxxxxxxxxx'
    port = 'xxxxxxxxxx'

    # create capture
    capture = cv2.VideoCapture(
        f'rtsp://{username}:{password}@{ip}:{port}/live.sdp')

    #get information
    height = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    width = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv2.CAP_PROP_FPS)

    #get image
    while True:
        start = time()
        ret, img = capture.read()  #the img color order is BGR
        end = time()
        print(end - start)
        print(1 / (end - start))
        cv2.imshow(f'Video Height {height} Width {width} FPS {fps}', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
